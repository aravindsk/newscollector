import json
import datetime
import os
import glob
from time import gmtime, strftime
# from bson.json_util import dumps,loads
from bson import json_util

def write_to_data_file(entry_list,file_ts):
    directory_path = "datafiles/"+entry_list[0]['source_site']
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


    filename = directory_path +'/' + entry_list[0]['source_site'] +file_ts + ".json"

    with open(filename, 'w') as outfile:
        #create mongoDB formatted JSON from dict
        # mongo_spec = json_util.dumps(entry_list)
        # bson = json.dumps(entry_list, default=json_util.default)
        json.dump(entry_list, outfile)
        # json_util.dumps(entry_list, outfile)


def write_to_data_file_from_dict(entry_list,file_ts):
    directory_path = "datafiles/"+entry_list['source_site']
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


    filename = directory_path +'/' + entry_list['source_site'] +file_ts + ".json"

    with open(filename, 'a') as outfile:
        #create mongoDB formatted JSON from dict
        # mongo_spec = dumps(entry_list)
        # bson = json.dumps(entry_list, default=json_util.default)
        json.dump(entry_list, outfile)
        # json.dump(',', outfile)


def get_id_list_from_data_file(source_site):
    directory_path = 'datafiles/'
    path = directory_path+source_site
    id_list = list()

    #get filename each file in the directory for the site
    for filename in glob.glob(os.path.join(path, '*.json')):
        #open file
        with open(filename) as json_file:
            data = json.load(json_file)
        #get _id and append to list
            for article_list in data: #json_util.loads(data):
                id_list.append(article_list['_id'])
    return  id_list

def get_id_list_from_dict_data_file(source_site):
    directory_path = 'datafiles/'
    path = directory_path+source_site
    id_list = list()

    #get filename each file in the directory for the site
    for filename in glob.glob(os.path.join(path, '*.json')):
        #open file
        with open(filename) as json_file:
            data = json.load(json_file)
            #get _id and append to list
            for article_list in json_util.loads(data):
                id_list.append(article_list['_id'])
    return  id_list