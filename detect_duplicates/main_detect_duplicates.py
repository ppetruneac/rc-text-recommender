"""
Main function to detect duplicates. 
"""

import pandas as pd
import utils
import detect_duplicates
import os, yaml, argparse

# Get MySQL username and password via terminal arguments
parser = argparse.ArgumentParser(description='Get MySQL user and password.')
parser.add_argument('-u')
parser.add_argument('-p')

args = parser.parse_args()
user = args.u
password = args.p


# Get the config file
with open('config.yaml') as cred:
  config = yaml.safe_load(cred)

# Get parameters 
mysql_credentials = config['mysql_credentials']
interval = config['interval']
min_obs_lan = config['min_obs_lan']
dict_lan = config['dict_lan']
dict_res_type_id = config['dict_res_type_id']
resource_type2remove = config['resource_type2remove']
first_run = config['first_run']
verbose = config['verbose']
save_file_path = config['save_file_path']


# Reading data
if verbose:
  print("\nReading data for detecting duplicates ... ")
df_ref, df_latest, df_dup_validated = utils.read_data_duplicates(host=mysql_credentials['host'], 
                                              user=user, 
                                              password=password, 
                                              db=mysql_credentials['database'], 
                                              resource_type2remove = resource_type2remove,
                                              interval = interval)

if verbose:                                                      
  print("\tshape df_ref = {}".format(df_ref.shape))
  print("\tshape df_latest = {}".format(df_latest.shape))

# Cleaning the data
df_ref = utils.clean_data(df_ref, verbose = verbose,
                          save_file_path = save_file_path)
df_latest = utils.clean_data(df_latest,  verbose = verbose, 
                            save_file_path = save_file_path)


# Creating the tf vocabularily and save it to data/interim/tf
if first_run:
  df_combined = pd.concat([df_ref, df_latest], axis = 0)
  utils.get_term_frequency_voc(df_combined, dict_lan = dict_lan, 
                                  dict_res_type_id = dict_res_type_id,
                                  verbose = verbose, 
                                  save_file_path = save_file_path, 
                                  min_obs_lan=min_obs_lan)                             
 
#  Detect duplicates for new resources
duplicates = detect_duplicates.detect_duplicates(df_ref, df_latest, df_dup_validated,
                              dict_lan = dict_lan, 
                              verbose=verbose, 
                              save_file_path = save_file_path)