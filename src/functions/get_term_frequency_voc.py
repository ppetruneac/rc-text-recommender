#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import json, os, shutil
from langdetect import detect
from stop_words import get_stop_words
from sklearn.feature_extraction.text import CountVectorizer


def get_term_frequency_voc(df, verbose = False, save_file_path = "../../", min_obs_lan = 100):

  """
  Function to create the term frequency vocabulary for each type of resource type and language.  
  It will be later on used to detect duplicates and compute similar resources. 
  This code saves the tf vocabularily.
  
  Arguments
  ---------
    df : dataframe with columns [id, title, type, content]
    verbose : if to print progress
    save_file_path : controls how many levels up to go to the saving directory, data; it is not a full path 
    min_obs_lan : min obs to be considered per Type & Language. Default = 100, preferably to not change. 

  """   

  # Creating the language dictioanry using the language_id.
  # Language 'Romani (tiganeasca)' cannot be found in langdetect. 
  dict_lan = {'1': 'ro',
              '2': 'en',
              '3': 'fr',
              '4': 'it',
              '5': 'es',
              '6': 'de',
              '7': 'hu',
              '8': 'ru'}

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
      print('\n\tWorking on type {} out of {} (type {}) ... '.format(i+1, len(rc_type), type_))
      print("\tshape = {}".format(df_.shape))

    language = df['language_id'].unique()
    if verbose:
      print("\tThere are {} languages for type {}. ".format(len(language), type_))

    for j, lan in enumerate(language):
      # This if statement is to limited wrongly detected languages. 
      if (lan >= min_obs_lan):

        df_lang = df_[df_['language_id'] == lan]
        if verbose:
          print('\tWorking on language {} ... '.format(dict_lan[str(lan)]))

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
        if verbose:
          print('\t\tWriting vocabulary to disk ...')
      
        # Saving the vocabulary to file
        for v in vocabulary:
            vocabulary[v] = vocabulary[v].item()
        json_data = json.dumps(vocabulary)
        voc_name = save_file_path + "data/interim/tf_voc/tf_voc_"  + str(type_) + "_" + dict_lan[str(lan)] + '.json'
        f = open(voc_name,"w")
        f.write(json_data)
        f.close()

        if verbose:
          print('\t\tVocabulary was written to: {}'.format(voc_name))

  if verbose:
    print("\nVocabulary for {} resources was written to {}. ".\
      format(len(rc_type), save_file_path + "data/interim/tf_voc/"))
  