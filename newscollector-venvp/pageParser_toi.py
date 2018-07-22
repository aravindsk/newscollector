import requests
import pytz,datetime
from bs4 import BeautifulSoup
import sys
def scrapeURLTOI(input_url,published_time):
    article_info = dict()
    try:
        siteTimeZone = pytz.timezone ("Etc/GMT")
        pubTime = datetime.datetime.strptime(published_time.rsplit(' GMT')[0].rsplit(', ')[1],'%d %b %Y %H:%M:%S')
        pubTimeUTC = siteTimeZone.localize(pubTime, is_dst=None).astimezone(pytz.utc)
        article_info['publishTimeUTC']=pubTimeUTC

        page = requests.get(input_url)
        newsPage = BeautifulSoup(page.text, 'html.parser')
        
        classNameForArticle = 'Normal'
        articleDiv = newsPage.find("div", class_=classNameForArticle)
        article_info['articleText']=articleDiv.text
        return(article_info)
        
    except Exception as e:
        article_info['articleText']="Error in page parsing"
        return(article_info)
