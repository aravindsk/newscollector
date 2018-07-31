import sys
import ast
import copy
import feedparser
import requests
import pytz
import datetime
import os
from bs4 import BeautifulSoup
from pprint import pprint
from time import gmtime, strftime

from bson import Binary, Code
# from bson.json_util import dumps , RELAXED_JSON_OPTIONS,STRICT_JSON_OPTIONS
# from bson import json_util
from bson import json_util, EPOCH_AWARE, EPOCH_NAIVE, SON
from bson.json_util import (DatetimeRepresentation,
                            STRICT_JSON_OPTIONS)

import json

import pageParser_hindu
import pageParser_ndtv
import pageParser_hindustan_times
import pageParser_toi
import pageParser_tnm
import dbOps
import dataFileOps



def get_article_details(source_site,article_url,published_ts):
    if source_site == 'thehindu':
        # entry_dict['articleText'] = scrapeURLTheHindu(article_url)
        article_details_dict = pageParser_hindu.scrape_url_the_hindu(article_url, published_ts)
    elif source_site == 'hindustantimes':
        article_details_dict = pageParser_hindustan_times.scrape_url_hindustan_times(article_url, published_ts)
    elif source_site == 'ndtv':
        article_details_dict = pageParser_ndtv.scrape_url_ndtv(article_url, published_ts)
    elif source_site == 'toi':
        article_details_dict = pageParser_toi.scrape_url_toi(article_url, published_ts)
    elif source_site == 'thenewsminute':
        article_details_dict = pageParser_tnm.scrape_url_tnm(article_url, published_ts)
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

def build_all_sites_url_list():
    url_dict = dict()
    all_site_url_list = list()
    try:
        site_full_url_list = [{'site': 'thehindu', 'url': 'https://www.thehindu.com/rssfeeds/'},
                              {'site': 'thenewsminute', 'url': 'https://www.thenewsminute.com/rss-feeds'},
                              {'site': 'toi', 'url': 'https://timesofindia.indiatimes.com/rss.cms'},
                              {'site': 'hindustantimes', 'url': 'https://www.hindustantimes.com/rss/india/rssfeed.xml'},
                              {'site': 'ndtv', 'url': 'https://www.ndtv.com/rss'}
                              ]
        for site in site_full_url_list:
            if site['site']=='thehindu':
                all_site_url_list = pageParser_hindu.get_all_rss_feel_links(site['url'])
            if site['site'] == 'thenewsminute':
                all_site_url_list = pageParser_tnm.get_all_rss_feel_links(site['url'])
            if site['site'] == 'toi':
                all_site_url_list = pageParser_toi.get_all_rss_feel_links(site['url'])
            if site['site'] == 'ndtv':
                all_site_url_list = pageParser_ndtv.get_all_rss_feel_links(site['url'])
            if site['site'] == 'hindustantimes':
                all_site_url_list.clear()
                all_site_url_list.append(site['url'])

            read_rss(site['site'],all_site_url_list)


        return all_site_url_list

    except Exception as e:
        print('could not build URL list')
        raise

def read_rss(source_site,all_urls_for_site):
    try:
        for rssLink in all_urls_for_site:
            # get list of articles already processed and saved
            id_list_from_file = dataFileOps.get_article_id_from_file()
            article_id_list = list()

            # id_list_from_file = dataFileOps.get_id_list_from_data_file(rssLink['site'])
            filename_ts = strftime("_%Y_%m_%d_%H_%M", gmtime())

            entries_list = list()
            entry_dict = dict()
            d = feedparser.parse(rssLink)

            for entry in d.entries:

                # author not present in TOI
                # entry_dict['author'] = entry['author']
                entry_dict['title'] = entry['title']
                entry_dict['summary'] = entry['summary']
                entry_dict['link'] = entry['link']
                entry_dict['source_site'] = source_site
                entry_dict['_id'] = get_article_id(entry_dict['source_site'], entry_dict['link'])

                article_details_dict = None

                # check if execution on Rasp Pi or not.
                # If yes, do file ops.
                # Else do DB ops.
                # if os.uname()[4].startswith("arm"):
                    # check if ID already present in db. If yes, do not scrap URL and upsert
                if os.uname()[4].startswith("arm"):
                    if entry_dict['_id'] not in id_list_from_file:
                        print('datafile parse needed: ' + entry_dict['_id'])

                        article_details_dict = get_article_details(source_site, entry_dict['link'], entry['published'])
                        entry_dict['articleText'] = article_details_dict['articleText']
                        # entry_dict['published'] = article_details_dict['publishTimeUTC']

                        #fix needed for timezone conversion. now storing as GMT?
                        temp_string = json_util.dumps(article_details_dict['publishTimeUTC'], json_options=json_util.JSONOptions(tz_aware=True))
                        #convert string to dict and store
                        entry_dict['published'] = ast.literal_eval(temp_string)
                        entry_dict['logInsertTime'] = ast.literal_eval(json_util.dumps(datetime.datetime.utcnow(), json_options=json_util.JSONOptions(tz_aware=True)))
                        entry_dict['dataInsertType'] = 'fileImportToDB'

                        #build list of dicts to be written to JSON file
                        temp_dict = copy.deepcopy(entry_dict)
                        entries_list.append(temp_dict)

                        article_id_list.append(temp_dict['_id'])

                elif not os.uname()[4].startswith("arm"):
                    if not dbOps.checkDBforId(entry_dict['_id']):
                        print('mongo parse needed: ' + entry_dict['_id'])

                        article_details_dict = get_article_details(source_site, entry_dict['link'], entry['published'])
                        entry_dict['articleText'] = article_details_dict['articleText']
                        entry_dict['published'] = article_details_dict['publishTimeUTC']
                        entry_dict['dataInsertType'] = 'directWriteToDB'
                        #write each dict to DB. Consider bulk writing a list
                        dbOps.upsertToDB(entry_dict)


            # if list not empty, write to file
            if len(entries_list)>0:
                dataFileOps.write_to_data_file(entries_list,filename_ts)

            #update article_id file for lookup in next run
            dataFileOps.file_update_article_id(article_id_list)
    except Exception as e:
        print('error caught in read_rss')

if __name__ == '__main__':
    build_all_sites_url_list()
