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

  if verbose:
    print('\nGenerating the term frequency vocabulary ... ')

  # If dir found, remove it + fresh start. Create if not found. 
  model_output_path = save_file_path + "data/interim/tf_voc/"
  if os.path.exists(model_output_path):
    shutil.rmtree(model_output_path, ignore_errors = True)
    os.makedirs(model_output_path)
  else:
    os.makedirs(model_output_path)

  # if verbose:
  #   print('\tDetecting the language for all data (it can take a while) ... ')

  rc_type = df['type'].unique()
  # For each resource type, generate the tf and the vocabularily. 
  for i, type_ in enumerate(rc_type):
    df_ = df[df['type'] == type_].reset_index()

    if verbose:
      print('\n\tWorking on type {} out of {} (type {}) ... '.format(i+1, len(rc_type), type_))
      print("\tshape = {}".format(df_.shape))
      print('\t\tDetecting the language ... ')

    language = df_['content'].apply(lambda x: detect(x) if x != None else np.nan)
    df_.loc[df_.index, 'language'] = np.array(language)
    language = df_['language'].value_counts()

    if verbose:
      print("\t\tThere are {} languages for type {}. Only languages with > {} obs will be considered.".\
        format(len(language), type_, min_obs_lan))

    if len(language) == 1: 
      documents = df_['content']

      # Tries to get stopwords if found; if not will not remove them. 
      try: 
          cv = CountVectorizer(min_df=5, stop_words = get_stop_words(language.index.item()), max_features=10000)
      except:
          cv = CountVectorizer(min_df=5, max_features=10000) 
          
      tf_features = cv.fit_transform(documents).toarray()
      # tf_features = pd.DataFrame(tf_features, index=documents.index)

      vocabulary = cv.vocabulary_

      # Saving the vocabulary to file
      if verbose:
        print('\tWriting vocabulary to disk ...')
              
      for v in vocabulary:
          vocabulary[v] = vocabulary[v].item()
      json_data = json.dumps(vocabulary)
      voc_name = save_file_path + "data/interim/tf_voc/tf_voc_" + str(type_) + "_" + language.index.item() + '.json'
      f = open(voc_name,"w")
      f.write(json_data)
      f.close()

      if verbose:
        print('\t\tVocabulary was written to: {}'.format(voc_name))

    # If there are more languages, write tf for each languages with more than 100 items.
    else:
      lang_index = language.index
      for i, lan in enumerate(language):
        # This if statement is to limited wrongly detected languages. 
        if (lan >= min_obs_lan):
          df_lang = df_[df_['language'] == lang_index[i]]  
          if verbose:
            print('\t\tWorking on language {} ... '.format(lang_index[i].upper()))

          # This will be run once to create the tf-idf matrix and similarity df
          documents = df_lang['content']

          # Tries to get stopwords if found; if not will not remove them. 
          try: 
              cv = CountVectorizer(min_df=5, stop_words = get_stop_words(language.index.item()), max_features=10000)
          except:
              cv = CountVectorizer(min_df=5, max_features=10000) 

          tf_features = cv.fit_transform(documents).toarray()
          # tf_features = pd.DataFrame(tf_features, index=documents.index)

          vocabulary = cv.vocabulary_
          if verbose:
            print('\t\t\tWriting vocabulary to disk ...')
        
          # Saving the vocabulary to file
          for v in vocabulary:
              vocabulary[v] = vocabulary[v].item()
          json_data = json.dumps(vocabulary)
          voc_name = save_file_path + "data/interim/tf_voc/tf_voc_"  + str(type_) + "_" + lang_index[i] + '.json'
          f = open(voc_name,"w")
          f.write(json_data)
          f.close()

          if verbose:
            print('\t\t\tVocabulary was written to: {}'.format(voc_name))

  if verbose:
    print("\nVocabulary for {} resources was written to {}. ".\
      format(len(rc_type), save_file_path + "data/interim/tf_voc/"))
  