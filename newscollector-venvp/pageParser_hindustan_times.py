import requests
import pytz,datetime
from bs4 import BeautifulSoup

def scrapeURLHindustanTimes(input_url,published_time):
    article_info = dict()
    # xxx/story-FHE8dJuI0yk7UQ3ZvrDEAK.html
    try:
        siteTimeZone = pytz.timezone ("Etc/GMT")
        pubTime = datetime.datetime.strptime(published_time.rsplit(' GMT')[0].rsplit(', ')[1],'%d %b %Y %H:%M:%S')
        pubTimeUTC = siteTimeZone.localize(pubTime, is_dst=None).astimezone(pytz.utc)
        article_info['publishTimeUTC']=pubTimeUTC
        

        page = requests.get(input_url)
        newsPage = BeautifulSoup(page.text, 'html.parser')
        classNameForArticle = 'story-details'
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