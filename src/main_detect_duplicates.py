

import pandas as pd
from functions import clean_data
from functions import get_term_frequency_voc
from functions import detect_duplicates
import os

first_run = True
# first_run : boolean. If True it will create data/interim/tf_voc folder

sudo_password = 'sudo_password'

print('\nReading data from MySQL ... ')
# ===============CHANGE__THIS__SQL__FILE: make_dataset_duplicates.sql ===============
bashCommand = "echo " + sudo_password + "  | sudo mysql --user=root  < functions/make_dataset_duplicates.sql"
os.system(bashCommand)

# Move the files from /tmp folder
bashCommand = "echo " + sudo_password + "| sudo mv /tmp/dataset_duplicates_all.csv ../data/sample/"
os.system(bashCommand)
bashCommand = "echo " + sudo_password + "| sudo mv /tmp/dataset_duplicates_latest.csv ../data/sample/"
os.system(bashCommand)

# Importing data in Python env
df_ref = pd.read_csv('../data/sample/dataset_duplicates_all.csv')
df_ref.columns = ['id', 'res_type_id', 'language_id', 'title', 'created_at', 'content']
print("\tshape df_ref = {}".format(df_ref.shape))

df_latest = pd.read_csv('../data/sample/dataset_duplicates_latest.csv')
df_latest.columns = ['id', 'res_type_id', 'language_id', 'title', 'created_at', 'content']
print("\tshape df_latest = {}".format(df_latest.shape))

# Cleaning the data
df_ref = clean_data.clean_data(df_ref, verbose = True, write = False, save_file_path = "../")
df_latest = clean_data.clean_data(df_latest, verbose = True, write = False, save_file_path = "../")

# Creating the tf vocabularily and save it to data/interim/tf
if first_run:
  df_combined = pd.concat([df_ref, df_latest], axis = 0)
  get_term_frequency_voc.get_term_frequency_voc(df_combined, verbose = True, save_file_path = "../")
 
#  Detect duplicates for new resources
duplicates = detect_duplicates.detect_duplicates(df_ref, df_latest, verbose=True, write = True, save_file_path = "../")

# Load new duplicates to MySQL
print('Loading the latest duplicates to MySQL ...')
bashCommand = "echo " + sudo_password + "  | sudo mysql --user=root  < functions/load_duplicates_to_MySQL.sql"
os.system(bashCommand)
print('DONE! ')