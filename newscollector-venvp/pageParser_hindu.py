import requests
import pytz,datetime
from bs4 import BeautifulSoup

def scrapeURLTheHindu(input_url,published_time):
    article_info = dict()
    #xxx/article24436479.ece
    try:
        siteTimeZone = pytz.timezone ("Asia/Kolkata")
        pubTime = datetime.datetime.strptime(published_time.rsplit(' +')[0].rsplit(', ')[1],'%d %b %Y %H:%M:%S')
        pubTimeUTC = siteTimeZone.localize(pubTime, is_dst=None).astimezone(pytz.utc)
        article_info['publishTimeUTC']=pubTimeUTC

        page = requests.get(input_url)
        newsPage = BeautifulSoup(page.text, 'html.parser')
        
        classNameForArticle = 'article'
        articleDiv = newsPage.find("div", class_=classNameForArticle)
        allParas = articleDiv.findAll("p")
        textInPara = ''
        for p in allParas:
            textInPara = textInPara+p.getText()

        # print(textInPara)
        article_info['articleText']=textInPara
        return(article_info)    

    except Exception as e:
        article_info['articleText']="Error in page parsing"
        return(article_info)