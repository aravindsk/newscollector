#sftp files onto server

import os
import pysftp
import sys

def transfer_files(input_source_directory):

    target_path = '/home/sk/coding/newscollector/newscollector-venvp/datafiles/staging'
    local_directory_path = input_source_directory

    host = "10.0.0.2"
    username = "sk"
    password = "ubuntupass"

    #set for ssh authentication. Review.
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    for root,dirs,files in os.walk(local_directory_path):
        for filename in files:
            filepath = root + '/' + filename
            if filepath.rsplit('.',1)[-1]=='json':
                print(root + '/' + filename)
                local_file_name = root + '/' + filename
                target_file_name = target_path + '/' + filename

                with pysftp.Connection(host, username=username, password=password, cnopts=cnopts) as sftp:
                    sftp.put(local_file_name, target_file_name)

    print ('Upload done.')


if __name__ == '__main__':
    source_directory = 'datafiles/staging'
    transfer_files(source_directory)

