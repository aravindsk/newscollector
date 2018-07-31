import json
import datetime
import os
import glob
from time import gmtime, strftime
from bson import json_util
import csv

current_directory_path = os.path.abspath(os.path.dirname(__file__))

def file_update_article_id(list_article_id):
    global current_directory_path
    file_path = os.path.join(current_directory_path, 'datafiles/article_ids.csv')
    with open(file_path, 'a', newline='') as csvfile:

        for article_id in list_article_id:
            csvfile.write(article_id)
            csvfile.write('\n')

def get_article_id_from_file():
    file_path = os.path.join(current_directory_path,'datafiles/article_ids.csv')
    list_article_id = list()
    with open(file_path, "r") as f:
        reader = csv.reader(f, delimiter="\n")
        for line in (reader):
            list_article_id.append(line[0])
    return list_article_id

def write_to_data_file(entry_list,file_ts):
    global current_directory_path
    relative_directory_path = "datafiles/staging/"+entry_list[0]['source_site']
    directory_path = os.path.join(current_directory_path,relative_directory_path)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


    filename = directory_path +'/' + entry_list[0]['source_site'] +file_ts + ".json"

    with open(filename, 'w') as outfile:
        json.dump(entry_list, outfile,indent=4,sort_keys=True)




#deprecated : replaced by get_article_id_from_file
def get_id_list_from_data_file(source_site):
    global current_directory_path
    relative_directory_path = 'datafiles/staging/'
    directory_path = os.path.join(current_directory_path, relative_directory_path)
    path = directory_path+source_site
    id_list = list()

    #get filename each file in the directory for the site
    for filename in glob.glob(os.path.join(path, '*.json')):
        #open file
        with open(filename) as json_file:
            data = json.load(json_file)
        #get _id and append to list
            for article_list in data:
                id_list.append(article_list['_id'])
    return  id_list
