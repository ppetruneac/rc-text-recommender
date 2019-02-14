

import pandas as pd
# from functions import clean_data
# from functions import get_term_frequency_voc
import os

# If reading the data from real MySQL db, change to False. If True, will upload sample data into db
# for demo purpose. 
test_mode = False

# Indicate if this is the first run. This will create: data/interim/tf_voc folder. 
#  Change to `False` if not the first run.
first_run = True

if test_mode:
  # Create a sample db with sample data.  
  print('Creating a sample db (resurse_crestine) in MySQL ... ')
  bashCommand = "mysql  --user=root  < functions/create_mysql_db_test_mode.sql"
  os.system(bashCommand)

if first_run:
  print('Reading ALL data from MySQL ... ')
  bashCommand = "mysql  --user=root  < functions/make_dataset_first_run.sql"
  os.system(bashCommand)

  os.listdir("../data/sample/")
# else:
  # Is not the first run
  # make_dataset.py --> read sample data from MySQL + save to sample/data/new_resources.csv



# print("\nReading data ... ")
# df = pd.read_csv('../data/sample/tilda_separated.csv', delimiter='~')

# # Cleaning the data
# df = clean_data.clean_data(df, verbose = True, write = True, save_file_path = "../")

# # Creating the tf vocabularily and save it to data/interim/tf
# if first_run:
#   get_term_frequency_voc.get_term_frequency_voc(df, verbose = True, save_file_path = "../")