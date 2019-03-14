

import pandas as pd
from functions import clean_data
from functions import get_term_frequency_voc
from functions import detect_duplicates
from functions import make_dataset_duplicates
import os

first_run = True
# first_run : boolean. If True it will create data/interim/tf_voc folder

# Reading data
print("\nReading the data ... ")
df_ref, df_latest = make_dataset_duplicates.read_data(host='host', user='root', password='password', db='db')
print("\tshape df_ref = {}".format(df_ref.shape))
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
bashCommand = "sudo mysql --user=root  < functions/load_duplicates_to_MySQL.sql"
os.system(bashCommand)
print('DONE! ')