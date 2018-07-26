#write from datafile to mongodb
#after success move files from staging to completed folders

import sys
import subprocess
import os
import glob
# from dbConnectionProp import dbConnection


def move_file_after_process(input_file_path,process_status):
    filename = input_file_path.rsplit('/',1)[-1]
    if process_status == 0:
        os.rename(input_file_path, "../datafiles/processed/completed/"+filename)
    if process_status == 1:
        os.rename(input_file_path, "../datafiles/processed/failed/"+filename)

def run_mongoimport_on_file(file_path):
    db_host = '10.0.0.2:27017'
    db_name = 'news_articles'
    db_collection_name = 'articlestest'

    result_subprocess = subprocess.run(
        ['mongoimport', '--host', db_host , '--db', db_name, '-c', db_collection_name , '--mode', 'upsert',
         '--jsonArray', '--file', file_path])


    #result_subprocess.returncode == 0 : subprocess success
    #result_subprocess.returncode == 1 : subprocess fail
    move_file_after_process(file_path,result_subprocess.returncode)

def process_files(input_directory_path):
    directory_path = input_directory_path
    # path = directory_path+source_site
    #
    # get filename each file in the directory for the site
    # for filename in glob.glob(os.path.join(path, '*.json')):

    for root,dirs,files in os.walk(directory_path):
        for filename in files:
            filepath = root + '/' + filename
            if filepath.rsplit('.',1)[-1]=='json':
                print(root + '/' + filename)
                run_mongoimport_on_file(filepath)



if __name__ == '__main__':
    process_files('../datafiles/staging')
