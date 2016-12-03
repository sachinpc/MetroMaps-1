"""
  Usage: gen_config.py <path to folder containing raw data files>

  This application  gets the list of all raw_file names of the form <dataset_id>_<data_id>.txt"
  and autogenerates config.json. An existing config.json will be renamed with a timestamp attached to it.

  Example:
      A folder "/tmp/raw_data" contains data for 3 books with 2 chapters named as 
      1_1.txt 1_2.txt 2_1.txt 2_2.txt 3_1.txt 3_2.txt

      commandprompt$> python gen_config.py /tmp/raw_data
 
      will generate config.json with data  {"1":[1,2], "2":[1,2], "3":[1,2]}

"""
import sys
import re
from os import listdir
from os.path import isfile, join
import os.path
import json
from collections import defaultdict
import datetime

pattern = re.compile(r'(\d+)_(\d+).txt')

def get_list_of_files( mypath ):
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles

def gen_json( files, cfgfile_name ):
    cluster_dir = defaultdict(list)
    for fname in files:
        parts = re.search( pattern, fname )  
        if parts  != None:
            cluster_id = parts.group(1)
            doc_id = int(parts.group(2))
            cluster_dir[cluster_id].append(doc_id)
   

    # backup old files
    if os.path.isfile( cfgfile_name ):
       newfname =  "_".join(str(datetime.datetime.now()).split())
       os.rename( cfgfile_name, "_".join([cfgfile_name , newfname]) )

    # create config file
    with open(cfgfile_name, 'w') as fp:
        json.dump(cluster_dir, fp)

        
if __name__ == "__main__":
   if len(sys.argv) < 2:
       print("Usage:  commandprompt$> python gen_config.py <path_to_folder_containing_raw_data_dir>")
   else:   
       data_dir = sys.argv[1]
       files = get_list_of_files( data_dir )
       confg_file = gen_json( files , "config.json" )
       print(files)
   

   

