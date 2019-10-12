"""

Main function to detect duplicates. 
"""

import pandas as pd
from functions import rc_utils
from functions import detect_duplicates
import os, yaml


# Defining paarameters
first_run = False # boolean. If True it will create data/interim/tf_voc folder; Set True for first run. Also recommended to be True at least once a month.
save_file_path = '../' # controls path levels where to save the data
verbose = True
min_obs_lan = 100 # min observations per language to be able to detect duplicates. 

# Get the MySQL connection credentials from file
with open('credentials_db.yaml') as cred:
  credentials = yaml.safe_load(cred)

# Creating the language dictioanry using the language_id. 
# Language 'Romani (tiganeasca)' cannot be found in langdetect. 
dict_lan = {'1': 'ro',
            '2': 'en',
            '3': 'fr',
            '4': 'it',
            '5': 'es',
            '6': 'de',
            '7': 'hu',
            '8': 'ru',
            '9':'unknown1', 
            '10': 'unknown2'}

# `res_type_id` that are not of type text/string.
resource_type2remove = [15,17,18,20,22,30,31,29,40,48,35,12]            

# Reading data
print("\nReading the data for duplicates ... ")
df_ref, df_latest = rc_utils.read_data_duplicates(host=credentials['host'], 
                                                      user=credentials['username'], 
                                                      password=credentials['password'], 
                                                      db=credentials['database'], 
                                                      interval = 3400)
print("\tshape df_ref = {}".format(df_ref.shape))
print("\tshape df_latest = {}".format(df_latest.shape))

# Cleaning the data
df_ref = rc_utils.clean_data(df_ref, 
                            resource_type2remove = resource_type2remove,
                            verbose = verbose, 
                            write = False, 
                            save_file_path = save_file_path)
df_latest = rc_utils.clean_data(df_latest, 
                            resource_type2remove = resource_type2remove,
                            verbose = verbose, 
                            write = False, 
                            save_file_path = save_file_path)


# Creating the tf vocabularily and save it to data/interim/tf
if first_run:
  df_combined = pd.concat([df_ref, df_latest], axis = 0)
  rc_utils.get_term_frequency_voc(df_combined, dict_lan = dict_lan, 
                                  verbose = verbose, 
                                  save_file_path = save_file_path, 
                                  min_obs_lan=min_obs_lan)
 
#  Detect duplicates for new resources
duplicates = detect_duplicates.detect_duplicates(df_ref, df_latest, dict_lan = dict_lan, verbose=verbose, write = True, save_file_path = save_file_path)

# # Load new duplicates to MySQL
print('Loading the latest duplicates to MySQL ...')
bashCommand = 'mysql --user=' + credentials['username'] + ' --password=' +  credentials['password'] + ' < functions/load_duplicates_to_MySQL.sql'
os.system(bashCommand)

print('DONE! ')