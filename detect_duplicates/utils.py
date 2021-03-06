
"""
Util fucntions for resurese crestine text recommender project. 

"""

import pymysql
import pandas as pd
import re, string, time
import numpy as np
import json, os, shutil
from langdetect import detect # initially used to detect the language, but now comes with the data. 
from stop_words import get_stop_words
from sklearn.feature_extraction.text import CountVectorizer


def read_data(host, user, password, db, resource_type2remove, interval=24):
  
  """
  Function that reads data from MySQL and returns 3 data frames: 
    - one with all data but not the last X (e.g. 24 hours)
    - the 2nd one containing data in the last X (24) hours.
    - the 3rd one is the validated duplicates in the database.

  Arguments:
  ----------
  host : your host, usually localhost
  user : your username
  passwd : your password
  db : database name to be used
  resource_type2remove : resource type as it apperas in `res_type_id` and needs not to be included. 
  interval : int; interval in terms of hour e.g. 24h -- it reads data in the last 24h and computes duplicates. 

  Output:
  -------
  df_ref and df_latest : df containing reference and latest data. 
  """

  connection = pymysql.connect(host=host, user=user, passwd=password,db=db) 
  cursor = connection.cursor()

  query_ref = """
    SELECT
      resources.id,
      resources.res_type_id,
      resources.language_id,
      resources.title,
      text_details.content  
    FROM
      resources
    LEFT JOIN text_details ON resources.id = text_details.resources_id
    WHERE
      text_details.content is not null and resources.created_at < (NOW() - INTERVAL """ + str(interval) + " HOUR) and  resources.res_type_id not in (""" + ', '.join([str(el) for el in resource_type2remove]) + ") "
  
  df_ref = pd.read_sql(query_ref, connection)

  query_latest = """
    SELECT
      resources.id,
      resources.res_type_id,
      resources.language_id,
      resources.title,
      text_details.content  
    FROM
      resources
    LEFT JOIN text_details ON resources.id = text_details.resources_id
    WHERE
      text_details.content is not null and resources.created_at > (NOW() - INTERVAL """ + str(interval) + " HOUR) and  resources.res_type_id not in (""" + ', '.join([str(el) for el in resource_type2remove]) + ") "

  df_latest = pd.read_sql(query_latest, connection)

  query_duplicates_validated = """
    SELECT 
    res_type_id,
      language_id, 
      min(cos_similarity) as cos_similarity_min,
      max(cos_similarity) as cos_similarity_max,
      std(cos_similarity) as cos_similarity_std,
    min(content_distance) as content_distance_min,
      max(content_distance) as content_distance_max,
      std(content_distance) as content_distance_std,
    min(title_distance) as title_distance_min,
      max(title_distance) as title_distance_max,
      std(title_distance) as title_distance_std
    FROM resursenew.duplicates_validated
    where certainty = 'validated'
    group by 1,2
  """
  df_dup_validated = pd.read_sql(query_duplicates_validated, connection)

  connection.close()

  return df_ref, df_latest, df_dup_validated


def clean_data(df,  verbose = False, write = False, 
                write_filename = 'dataset_clean',
                save_file_path = "../../"):

  """

  Function reads data + cleans the text data. 
  - makes assumptions as what data / resources to keep
  - cleans the data (title & content / body): 
      1. removes diacritice
      * removes html tags & encoding
      *  Remove /n, /r etc
      * Remove words of length 1 & non-alphabetical characters
  - saves the clean data
  
  Arguments:
  ===========
    df: dataframe with columns [id, title, res_type_id, content]
    resource_type2remove : resource type as it apperas in `res_type_id` and needs not to be included. 
    verbose: if to print progress
    write =  boolean, whether to save the file to data folder or not.
    save_file_path: controls how many levels up to go to the saving directory, data; it is not a full path 


  """

  # ## Data Cleaning

  if verbose:
    print("Cleaning data ... ")

  # Strip the missing values. 
  if verbose:
    print("\tStripping data with missing values ... ")
  df = df[(~df['title'].isna()) & (~df['content'].isna()) & (~df['res_type_id'].isna())]

  # Lower case the text fields
  if verbose:
    print("\tLower case the text data ... ")
  df['title'] = df['title'].str.lower()
  df['content'] = df['content'].str.lower()
  
  # ### Remove Diacritice
  if verbose:
    print("\tRemoving diacritice ... ")
  df['title'] = df['title'].\
    apply(lambda x: x.replace('??','a')).\
    apply(lambda x: x.replace('??','a')).\
    apply(lambda x: x.replace('??','i')).\
    apply(lambda x: x.replace('??','s')).\
    apply(lambda x: x.replace('??','s')).\
    apply(lambda x: x.replace('??','t')).\
    apply(lambda x: x.replace('??','t'))

  df['content'] = df['content'].\
    apply(lambda x: x.replace('??','a')).\
    apply(lambda x: x.replace('??','a')).\
    apply(lambda x: x.replace('??','i')).\
    apply(lambda x: x.replace('??','s')).\
    apply(lambda x: x.replace('??','s')).\
    apply(lambda x: x.replace('??','t')).\
    apply(lambda x: x.replace('??','t'))
      
  # ### Remove html tags & encoding
  if verbose:
    print("\tRemoving html tags and encoding ... ")
  def remove_html_tags(text):
    """Remove html tags from a string. This is anything in between <>"""
    clean = re.compile('<.*?>')
    return re.sub(clean, ' ', text)
  def remove_html_encoding(text):
    """Remove html encodings from a string. This is anything that starts with '&' and ends with ';'"""
    clean = re.compile('&.*?;')
    return re.sub(clean, ' ', text)
  df['content'] = df['content'].apply(lambda x: remove_html_tags(x))
  df['content'] = df['content'].apply(lambda x: remove_html_encoding(x))

  # ### Remove `/n`, `/r` etc
  if verbose:
    print("\tRemoving more html characters ... ")
  def remove_n(text):
    """Remove \n """
    return re.sub(re.compile('\n'), ' ', text)
  def remove_t(text):
    """Remove \t """
    return re.sub(re.compile('\t'), ' ', text)
  def remove_b(text):
    """Remove \b """
    return re.sub(re.compile('\b'), ' ', text)
  def remove_r(text):
    """Remove \r """
    return re.sub(re.compile('\r'), ' ', text)

  df['content'] = df['content'].\
    apply(lambda x: remove_n(x)).\
    apply(lambda x: remove_t(x)).\
    apply(lambda x: remove_b(x)).\
    apply(lambda x: remove_r(x))

  # **Remove words of length 1 & non-alphabetical characters**
  if verbose:
    print("\tRemoving words of length 1 & non-alphabetical characters ... ")
  df['content'] = df['content'].\
    apply(lambda x: ''.join(ch for ch in x if ch not in string.punctuation)).\
    apply(lambda x: ' '.join(x.split())).\
    apply(lambda x: re.sub(r'[^a-zA-Z]', ' ', x)).\
    apply(lambda x: re.sub(r'\b\w{1}\b', '', x))

  df['title'] = df['title'].\
    apply(lambda x: ''.join(ch for ch in x if ch not in string.punctuation)).\
    apply(lambda x: ' '.join(x.split())).\
    apply(lambda x: re.sub(r'[^a-zA-Z]', ' ', x)).\
    apply(lambda x: re.sub(r'\b\w{1}\b', '', x))

  # Removing data that has length < 10 characters.
  if verbose:
    print("\tRemoving data that has length < 10 characters ... ")
    print("\tShape before = {}".format(df.shape))  

  filter_ = df['content'].apply(lambda x: len(x)) <=10
  df = df[~filter_]
  if verbose:
    print("\tShape after = {}".format(df.shape))  

  if write:
    filepath = save_file_path + 'data/interim/' + write_filename + '.csv'
    if verbose:
      print("\tWriting clean data {} ... ".format(filepath))
    df.to_csv(path_or_buf=filepath, header = True, index=False)

  if verbose:
    print("\tData Cleaning is finished! ")

  return df


def get_term_frequency_voc(df, dict_lan, dict_res_type_id, verbose = False, save_file_path = "../../", min_obs_lan = 100):
  
  """
  Function to create the term frequency vocabulary for each type of resource type and language.  
  It will be later on used to detect duplicates and compute similar resources. 
  This code saves the tf vocabularily.
  
  Arguments
  ---------
    df : dataframe with columns [id, title, type, content]
    dict_lan : dictionary that maps language integers to string; used in printing
    dict_res_type_id: dict to map resource type id to names
    verbose : if to print progress
    save_file_path : controls how many levels up to go to the saving directory, data; it is not a full path 
    min_obs_lan : min obs to be considered per Type & Language. Default = 100, preferably to not change. 

  """   

  if verbose:
    print('\nGenerating the term frequency vocabulary ... ')

  # If dir found, remove it + fresh start. Create if not found. 
  model_output_path = save_file_path + "data/interim/tf_voc/"
  if os.path.exists(model_output_path):
    shutil.rmtree(model_output_path, ignore_errors = True)
    os.makedirs(model_output_path)
  else:
    os.makedirs(model_output_path)

  rc_type = df['res_type_id'].unique()

  # For each resource type, generate the tf and the vocabularily. 
  for i, type_ in enumerate(rc_type):
    df_ = df[df['res_type_id'] == type_].reset_index()

    if verbose:
      print('\n\t`{}`: {} out of {};  shape = {} ... '.format(dict_res_type_id[str(type_)], i+1, len(rc_type), df_.shape))
      
    # only languages in the filtered df by type_
    language = df_['language_id'].unique()
  
    if verbose:
      print("\tThere are {} languages for type `{}`. It will only compute those with at least {} observations. ".format(len(language), dict_res_type_id[str(type_)], min_obs_lan))
    
    # For each language
    for j, lan in enumerate(language):
      df_lang = df_[df_['language_id'] == lan]
      
      if (df_lang.shape[0] >= min_obs_lan):        
        # This will be run once to create the tf-idf matrix and similarity df
        documents = df_lang['content']
        # Tries to get stopwords if found; if not will not remove them. 
        try: 
            cv = CountVectorizer(min_df=5, stop_words = get_stop_words(dict_lan[str(lan)]), max_features=10000)
        except:
            cv = CountVectorizer(min_df=5, max_features=10000) 

        tf_features = cv.fit_transform(documents).toarray()
        # tf_features = pd.DataFrame(tf_features, index=documents.index)

        vocabulary = cv.vocabulary_
      
        # Saving the vocabulary to file
        for v in vocabulary:
            vocabulary[v] = vocabulary[v].item()
        json_data = json.dumps(vocabulary)
        voc_name = save_file_path + "data/interim/tf_voc/tf_voc_"  + str(type_) + "_" + dict_lan[str(lan)] + '.json'
        f = open(voc_name,"w")
        f.write(json_data)
        f.close()

        if verbose:
          print('\t\t`{}` Vocabulary was written to: {}'.format(dict_lan[str(lan)].upper(), voc_name))
      else:
        if verbose:
          print('\t\tThere are not enough resources to compute voc for language `{}`.'.format(dict_lan[str(lan)]))
  
  if verbose:
    print("\n\tVocabulary for {} resources was written to {}. ".\
      format(len(rc_type), save_file_path + "data/interim/tf_voc/"))
  

if __name__ == "__main__":
  pass