import requests
import pytz
import datetime
from bs4 import BeautifulSoup

def scrape_url_toi(input_url,published_time):
    article_info = dict()
    try:
        site_time_zone = pytz.timezone ("Etc/GMT")
        pub_time = datetime.datetime.strptime(published_time.rsplit(' GMT')[0].rsplit(', ')[1],'%d %b %Y %H:%M:%S')
        pub_time_utc = site_time_zone.localize(pub_time, is_dst=None).astimezone(pytz.utc)
        article_info['publishTimeUTC']=pub_time_utc

        page = requests.get(input_url)
        news_page = BeautifulSoup(page.text, 'html.parser')
        
        class_name_for_article = 'Normal'
        article_div = news_page.find("div", class_=class_name_for_article)
        article_info['articleText']=article_div.text
        return article_info
        
    except Exception as e:
        article_info['articleText']="Error in page parsing"
        return article_info
