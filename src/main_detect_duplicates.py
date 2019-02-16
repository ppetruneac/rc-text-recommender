

import pandas as pd
from functions import clean_data
from functions import get_term_frequency_voc
from functions import detect_duplicates
import os

# If reading the data from real MySQL db, change to False. If True, will upload sample data into db
# for demo purpose. 
test_mode = False

# Indicate if this is the first run. This will create: ../data/interim/tf_voc folder. 
#  Change to `False` if not the first run.
first_run = False
sudo_password = 'pavdanawed2018'

if test_mode:
  # Create a sample db with sample data.  
  print('Creating a sample db (resurse_crestine) in MySQL ... ')
  bashCommand = "echo " + sudo_password + "  | sudo -S mysql --user=root  < functions/create_mysql_db_test_mode.sql"
  os.system(bashCommand) 


print('\nReading ALL data from MySQL apart from new resources (latest data)... ')
# ===============CHANGE__THIS__SQL__FILE===============
# bashCommand = "echo " + sudo_password + "  | sudo -S mysql --user=root  < functions/make_dataset_dup_all_data.sql"
# os.system(bashCommand)

# # Move the file from /tmp folder
# bashCommand = "echo " + sudo_password + "| sudo mv /tmp/dataset_duplicates_all.csv ../data/sample/"
# os.system(bashCommand)
# df = pd.read_csv('../data/sample/dataset_duplicates_all.csv')
# df.columns = ['id', 'title', 'type', 'content', 'datetime']
# df = df[['id', 'title', 'type', 'content']]
df_ref = pd.read_csv('../data/sample/tilda_separated.csv', delimiter='~')

print("Reading new resources (latest data) from MySQL ... ")
bashCommand = "echo " + sudo_password + "  | sudo -S mysql --user=root  < functions/make_dataset_dup_latest_data.sql"
os.system(bashCommand)
# Move the file from /tmp folder
bashCommand = "echo " + sudo_password + "| sudo mv /tmp/dataset_duplicates_latest.csv ../data/sample/"
os.system(bashCommand)
df_latest = pd.read_csv('../data/sample/dataset_duplicates_latest.csv')
df_latest.columns = ['id', 'title', 'type', 'content', 'datetime']
df_latest = df_latest[['id', 'title', 'type', 'content']]

# Cleaning the data
df_ref = clean_data.clean_data(df_ref, verbose = True, write = False, save_file_path = "../")
df_latest = clean_data.clean_data(df_latest, verbose = True, write = False, save_file_path = "../")

# Only for testing mode -- DELETE when read from actual MySQL.
# This will remove the latest resources (id level) from the all data. 
df_ref = df_ref[~df_ref['id'].isin(df_latest.id)]

# Creating the tf vocabularily and save it to data/interim/tf
if first_run:
  df_combined = pd.concat([df_ref, df_latest], axis = 1)
  get_term_frequency_voc.get_term_frequency_voc(df_combined, verbose = True, save_file_path = "../")
  
  # Create duplicates db
  bashCommand = "echo " + sudo_password + "  | sudo -S mysql --user=root  < functions/create_duplicates_db.sql"
  os.system(bashCommand)
 
#  Detect duplicates for new resources
duplicates = detect_duplicates.detect_duplicates(df_ref, df_latest, verbose=True, write = True, save_file_path = "../")

# Load new duplicates to MySQL
print('Loading the latest duplicates to MySQL ...')
bashCommand = "echo " + sudo_password + "  | sudo -S mysql --user=root  < functions/load_duplicates_to_MySQL.sql"
os.system(bashCommand)
print('DONE! ')