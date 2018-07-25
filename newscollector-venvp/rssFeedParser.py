import sys
import copy
import feedparser
import requests
import pytz
import datetime
import os
from bs4 import BeautifulSoup
from pprint import pprint

from pageParser_hindu import scrape_url_the_hindu
from pageParser_ndtv import scrape_url_ndtv
from pageParser_hindustan_times import scrape_url_hindustan_times
from pageParser_toi import scrape_url_toi
from pageParser_tnm import scrape_url_tnm
import dbOps
import dataFileOps



def get_article_details(source_site,article_url,published_ts):
    if source_site == 'thehindu':
        # entry_dict['articleText'] = scrapeURLTheHindu(article_url)
        article_details_dict = scrape_url_the_hindu(article_url, published_ts)
    elif source_site == 'hindustantimes':
        article_details_dict = scrape_url_hindustan_times(article_url, published_ts)
    elif source_site == 'ndtv':
        article_details_dict = scrape_url_ndtv(article_url, published_ts)
    elif source_site == 'toi':
        article_details_dict = scrape_url_toi(article_url, published_ts)
    elif source_site == 'thenewsminute':
        article_details_dict = scrape_url_tnm(article_url, published_ts)
    return article_details_dict
def get_article_id(source_site, input_url):
    try:
        article_id = 'unfetchable_default'
        if source_site == 'thehindu':
            article_id = 'thehindu_' + input_url.rsplit('/', maxsplit=1)[-1].rsplit('.')[0]
        elif source_site == 'hindustantimes':
            article_id = 'hindustantimes_' + input_url.rsplit('/', maxsplit=1)[-1].rsplit('-')[-1].rsplit('.')[0]
        elif source_site == 'ndtv':
            article_id = 'ndtv_' + input_url.rsplit('-', maxsplit=1)[-1]
        elif source_site == 'toi':
            article_id = 'toi_' + input_url.rsplit('/', maxsplit=1)[-1].rsplit('.')[0]
        elif source_site == 'thenewsminute':
            article_id = 'thenewsminute_' + input_url.rsplit('-', maxsplit=1)[-1]
        return article_id
    except Exception as e:
        print('could not find ID from URL')
        return None
        raise


def read_rss():

    feed_url_list = [
        {'site': 'thehindu', 'url': 'https://www.thehindu.com/news/national/feeder/default.rss'}
        ,
        {'site': 'toi', 'url': 'https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms'},
        {'site': 'hindustantimes', 'url': 'https://www.hindustantimes.com/rss/india/rssfeed.xml'},
        # # {'site':'deccanchronicle','url':'https://www.deccanchronicle.com/rss_feed/'},
        {'site': 'ndtv', 'url': 'https://feeds.feedburner.com/ndtvnews-india-news'},
        {'site': 'thenewsminute', 'url': 'https://www.thenewsminute.com/news.xml'}
    ]

    for rssLink in feed_url_list:
        id_list_from_file = dataFileOps.get_id_list_from_data_file(rssLink['site'])
        entries_list = list()
        entry_dict = dict()
        d = feedparser.parse(rssLink['url'])

        for entry in d.entries:

            # author not present in TOI
            # entry_dict['author'] = entry['author']
            entry_dict['title'] = entry['title']
            entry_dict['summary'] = entry['summary']
            entry_dict['link'] = entry['link']
            entry_dict['source_site'] = rssLink['site']
            entry_dict['_id'] = get_article_id(entry_dict['source_site'], entry_dict['link'])

            article_details_dict = None

            # check if execution on Rasp Pi or not.
            # If yes, do file ops.
            # Else do DB ops.
            # if os.uname()[4].startswith("arm"):
                # check if ID already present in db. If yes, do not scrap URL and upsert

            if not dbOps.checkDBforId(entry_dict['_id']) and not os.uname()[4].startswith("arm"):
            # if not os.uname()[4].startswith("arm"):
                print('mongo parse needed: ' + entry_dict['_id'])

                article_details_dict = get_article_details(rssLink['site'], entry_dict['link'], entry['published'])
                entry_dict['articleText'] = article_details_dict['articleText']
                entry_dict['published'] = article_details_dict['publishTimeUTC']
                #write each dict to DB. Consider bulk writing a list
                dbOps.upsertToDB(entry_dict)


            if  os.uname()[4].startswith("arm") and entry_dict['_id'] not in id_list_from_file:
                print('datafile parse needed: ' + entry_dict['_id'])

                article_details_dict = get_article_details(rssLink['site'], entry_dict['link'], entry['published'])
                entry_dict['articleText'] = article_details_dict['articleText']
                entry_dict['published'] = article_details_dict['publishTimeUTC']
                temp_dict = copy.deepcopy(entry_dict)
                entries_list.append(temp_dict)

        #if list not empty, write to file
        if len(entries_list)>0:
            dataFileOps.write_to_data_file(entries_list)

if __name__ == '__main__':
    read_rss()
