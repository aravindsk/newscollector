import sys
import copy
import feedparser
import requests
import pytz
import datetime
from bs4 import BeautifulSoup
from pprint import pprint

from pageParser_hindu import scrape_url_the_hindu
from pageParser_ndtv import scrape_url_ndtv
from pageParser_hindustan_times import scrape_url_hindustan_times
from pageParser_toi import scrape_url_toi
from pageParser_tnm import scrape_url_tnm
import dbOps


# import pymongo
# from pymongo import MongoClient
# from dbConnectionProp import dbConnection
# dbProp = dbConnection()
# mongoClient = MongoClient(dbProp.hostPath)
# mongoDb = mongoClient[dbProp.dbName]
# db_articles = mongoDb.articles

# article/google-teams-un-track-environmental-changes-employ-cloud-computing-84919


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
    # d = feedparser.parse('https://www.thehindu.com/news/national/feeder/default.rss')
    feed_url_list = [
        {'site': 'thehindu', 'url': 'https://www.thehindu.com/news/national/feeder/default.rss'},
        {'site': 'toi', 'url': 'https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms'},
        {'site': 'hindustantimes', 'url': 'https://www.hindustantimes.com/rss/india/rssfeed.xml'},
        # # {'site':'deccanchronicle','url':'https://www.deccanchronicle.com/rss_feed/'},
        {'site': 'ndtv', 'url': 'https://feeds.feedburner.com/ndtvnews-india-news'},
        {'site': 'thenewsminute', 'url': 'https://www.thenewsminute.com/news.xml'}
    ]

    for rssLink in feed_url_list:
        # entriesList = list()
        entry_dict = dict()
        d = feedparser.parse(rssLink['url'])
        # pprint(d)
        for entry in d.entries:
            # pprint(entry)
            # author not present in TOI
            # entry_dict['author'] = entry['author']
            entry_dict['title'] = entry['title']
            entry_dict['summary'] = entry['summary']
            entry_dict['link'] = entry['link']
            entry_dict['source_site'] = rssLink['site']
            entry_dict['_id'] = get_article_id(entry_dict['source_site'], entry_dict['link'])

            article_details_dict = None

            # check if ID already present in db. If yes, do not scrap URL and upsert
            print(entry_dict['_id'])

            if not dbOps.checkDBforId(entry_dict['_id']):
                print('parse needed: ' + entry_dict['_id'])

                if rssLink['site'] == 'thehindu':
                    # entry_dict['articleText'] = scrapeURLTheHindu(entry_dict['link'])
                    article_details_dict = scrape_url_the_hindu(entry_dict['link'], entry['published'])
                elif rssLink['site'] == 'hindustantimes':
                    article_details_dict = scrape_url_hindustan_times(entry_dict['link'], entry['published'])
                elif rssLink['site'] == 'ndtv':
                    article_details_dict = scrape_url_ndtv(entry_dict['link'], entry['published'])
                elif rssLink['site'] == 'toi':
                    article_details_dict = scrape_url_toi(entry_dict['link'], entry['published'])
                elif rssLink['site'] == 'thenewsminute':
                    article_details_dict = scrape_url_tnm(entry_dict['link'], entry['published'])

                entry_dict['articleText'] = article_details_dict['articleText']
                entry_dict['published'] = article_details_dict['publishTimeUTC']

                # pprint(entry_dict)
                dbOps.upsertToDB(entry_dict)
                # sys.exit()


if __name__ == '__main__':
    read_rss()
