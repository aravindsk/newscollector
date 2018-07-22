import requests
import pytz,datetime
from bs4 import BeautifulSoup

def scrapeURLNDTV(input_url,published_time):
    article_info = dict()

    try:
        # article_info['id']='ndtv_'+input_url.rsplit('-', maxsplit=1)[-1]
        # Tue, 17 Jul 2018 04:04:09 +0530
        # published_time
        # print(published_time.rsplit(' +')[0].rsplit(', ')[1])
        siteTimeZone = pytz.timezone ("Asia/Kolkata")
        pubTime = datetime.datetime.strptime(published_time.rsplit(' +')[0].rsplit(', ')[1],'%d %b %Y %H:%M:%S')
        pubTimeUTC = siteTimeZone.localize(pubTime, is_dst=None).astimezone(pytz.utc)
        article_info['publishTimeUTC']=pubTimeUTC

        page = requests.get(input_url)
        newsPage = BeautifulSoup(page.text, 'html.parser')
        
        classNameForArticle = 'ins_storybody'
        articleDiv = newsPage.find("div", class_=classNameForArticle)
        allParas = articleDiv.findAll("p")
        textInPara = ''
        for p in allParas:
            textInPara = textInPara+p.getText()

        article_info['articleText']=textInPara
        return(article_info)
    except Exception as e:
        article_info['articleText']="Error in page parsing"
        return(article_info)