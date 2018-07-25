import json
import datetime
import os
import glob
from time import gmtime, strftime
from bson.json_util import dumps,loads

def write_to_data_file(entry_list):
    directory_path = "datafiles/"+entry_list[0]['source_site']
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


    filename = directory_path +'/' + entry_list[0]['source_site'] + strftime("_%Y_%m_%d_%H_%M", gmtime()) + ".json"

    with open(filename, 'w') as outfile:
        #create mongoDB formatted JSON from dict
        mongo_spec = dumps(entry_list)
        json.dump(mongo_spec,outfile)

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
        for article_list in loads(data):
            id_list.append(article_list['_id'])
    return  id_list