#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import re, string, time
import swifter

def clean_data(df, verbose = False, write = False, save_file_path = "../../"):

  """
  Function reads data + cleans it. 
  - makes assumptions as what data / resources to keep
  - cleans the data (title & content / body): 
      1. removes diacritice
      * removes html tags & encoding
      *  Remove /n, /r etc
      * Remove words of length 1 & non-alphabetical characters
  - saves the clean data
  
  Input Arguments: 
    df: dataframe with columns [id, title, type, content]
    verbose: if to print progress
    write =  boolean, whether to save the file to data folder or not.
    save_file_path: controls how many levels up to go to the saving directory, data; it is not a full path 

  """

  # ## Data Cleaning

  if verbose:
    print("Cleaning the data ... ")

  # Lower case the text fields
  if verbose:
    print("\tLower case the text data ... ")
  df['title'] = df['title'].str.lower()
  df['content'] = df['content'].str.lower()

  # Strip the missing values. 
  if verbose:
    print("\tStripping the missing values ... ")
  df = df[(~df.title.isna()) & (~df.content.isna()) & (~df.type.isna())]

  # Remove resources of not type text
  if verbose:
    print("\tRemove resource type of not type `text` ... ")
  resource_type2remove = [15,17,18,20,22,30,31,29,40,48,35,12]
  df = df.loc[~df.type.isin(resource_type2remove)]
  
  # ### Remove Diacritice
  if verbose:
    print("\tRemoving diacritice ... ")
  df['title'] = df['title'].swifter.progress_bar(False).apply(lambda x: x.replace('â','a')).\
    apply(lambda x: x.replace('ă','a')).swifter.progress_bar(False).apply(lambda x: x.replace('î','i')).\
    apply(lambda x: x.replace('ș','s')).swifter.progress_bar(False).apply(lambda x: x.replace('ş','s')).\
    apply(lambda x: x.replace('ț','t')).swifter.progress_bar(False).apply(lambda x: x.replace('ţ','t'))
        
  df['content'] = df['content'].swifter.progress_bar(False).apply(lambda x: x.replace('â','a')).\
    apply(lambda x: x.replace('ă','a')).\
    apply(lambda x: x.replace('î','i')).\
    apply(lambda x: x.replace('ș','s')).\
    apply(lambda x: x.replace('ş','s')).\
    apply(lambda x: x.replace('ț','t')).\
    apply(lambda x: x.replace('ţ','t'))
      
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
  df['content'] = df['content'].swifter.progress_bar(False).apply(lambda x: remove_html_tags(x))
  df['content'] = df['content'].swifter.progress_bar(False).apply(lambda x: remove_html_encoding(x))

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

  df['content'] = df['content'].swifter.progress_bar(False).apply(lambda x: remove_n(x)).\
    apply(lambda x: remove_t(x)).\
    apply(lambda x: remove_b(x)).\
    apply(lambda x: remove_r(x))

  # **Remove words of length 1 & non-alphabetical characters**
  if verbose:
    print("\tRemoving words of length 1 & non-alphabetical characters ... ")
  df['content'] = df['content'].swifter.progress_bar(False).apply(lambda x: re.sub(r'\b\w{1}\b', '', x)).\
    apply(lambda x: re.sub(r'[^a-zA-Z]', ' ', x)).\
    apply(lambda x: ''.join(ch for ch in x if ch not in string.punctuation)).\
    apply(lambda x: ' '.join(x.split())) # removes whitespaces

  # Removing data that has length < 10 characters.
  if verbose:
    print("\tRemoving data that has length < 10 characters ... ")
    print("\t\tShape before = {}".format(df.shape))  

  filter_ = df['content'].swifter.progress_bar(False).apply(lambda x: len(x)) <=10
  df = df[~filter_]
  if verbose:
    print("\t\tShape after = {}".format(df.shape))  

  if write:
    filepath = save_file_path + 'data/interim/dataset_clean.csv'
    if verbose:
      print("\tWriting clean data {} ... ".format(filepath))
    df.to_csv(path_or_buf=filepath, header = True, index=False)

  if verbose:
    print("\tData Cleaning is DONE! ")

  return df

if __name__ == "__main__":
  df = clean_data(df, verbose = False, write = False, save_file_path = "../../")
