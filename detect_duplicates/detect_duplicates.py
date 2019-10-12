

import json, warnings
import numpy as np
import pandas as pd

from langdetect import detect
from tqdm import tqdm
from difflib import SequenceMatcher

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import MaxAbsScaler, Normalizer
from sklearn.pipeline import make_pipeline

warnings.simplefilter("ignore")

def similar_strings(a, b):
    return SequenceMatcher(None, a, b).ratio()

def duplicates_post_processing(duplicates, df_dup_validated, verbose=True):

  """
  Function to do duplicates post processing; 

  Assumptions
  -----------
    - duplicates duplicates dataframe.  
    - df_dup_validated : dataframe with duplicates validated. 
    - verbose : boolean; If True prints the progress; 
  """


  # Duplicates post processing

  if verbose:
    print('\tDuplicates post processing ... ')
  # Computing the distance between the content & title
  content_distance = []
  title_distance = []
  for i in range(duplicates.shape[0]):
      cd = similar_strings(duplicates.content[i], duplicates.content_dup[i])
      content_distance.append(cd)

      td = similar_strings(duplicates.title[i], duplicates.title_dup[i])
      title_distance.append(td)

  duplicates['content_distance'] = content_distance
  duplicates['title_distance'] = title_distance
  duplicates['certainty'] = 'unknown'



  #########

  # import pandas as pd
  # duplicates = pd.read_csv('../data/interim/duplicates_latest.csv')
  # df_dup_validated = pd.read_csv('../data/interim/df_dup_validated.csv')
  # duplicates['certainty'] = 'unknown'


  """
  Certainty is likely or unlikely, comparing cos_similarity, content_distance and title_distance.

  # Changing the certainty status based on min and max values of the validated duplicates +/- 1 std. 
  
  """

  for i, row in duplicates.iterrows():
  
    start = duplicates.loc[i, 'certainty']

    type_ = row['res_type_id']
    lan = row['language_id']

    filter_ = (df_dup_validated['res_type_id']== type_) & (df_dup_validated['language_id']== lan)
    ref = df_dup_validated[filter_] # validated duplicates reference 


    # Certainty likely
    k=0
    try:
      if (row['cos_similarity'] >= (ref['cos_similarity_max'] - 2*ref['cos_similarity_std'])).bool():
        k+=1
      elif (row['content_distance'] >= (ref['content_distance_max'] - 2*ref['content_distance_std'])).bool():
        k+=1
      elif (row['title_distance'] >= (ref['title_distance_max'] - 2*ref['title_distance_std'])).bool():
        k+=1

      if k >= 2:
        duplicates.loc[i, 'certainty'] = 'likely'
    except:
      None


    # Certainty unlikely
    k=0
    try:      
      if (row['cos_similarity'] <= (ref['cos_similarity_min'] - 1*ref['cos_similarity_std'])).bool():
        k+=1
      elif (row['content_distance'] <= (ref['content_distance_min'] - 1*ref['content_distance_std'])).bool():
        k+=1
      elif (row['title_distance'] <= (ref['title_distance_min'] - 1*ref['title_distance_std'])).bool():
        k+=1

      if k >= 2:
        duplicates.loc[i, 'certainty'] = 'uklikely'    
    except:
      None

    if verbose:
      print('\t\tDuplicate {} certainty change status: {} --> {}'.format(i, start, duplicates.loc[i, 'certainty']))

  
  duplicates = duplicates[['id', 'id_dup', 'res_type_id', 'language_id', 'title', 'title_dup', \
                          'content', 'content_dup', 'cos_similarity',  'content_distance', 'title_distance', 'certainty']]

  return duplicates    


def detect_duplicates(df_ref, df_latest, df_dup_validated, dict_lan, verbose=True, write = True, save_file_path = "../../"):
  """
  
  This function is being used to detect duplicates, or to generate the most similar resource to a given resource.

  Assumptions
  -----------
    - df_ref and df_latest will be clean before feeding into this function.  

  Parameters
  ---------- 
    - df_ref : dataframe with all resources; with columns [id, title, type, content]
    - df_latest : dataframe with latest resources to detect duplicates; with columns [id, title, type, content]
    - df_dup_validated : dataframe with duplicates validated. 
    - dict_lan : dictionary that maps language integers to string; used in printing
    - verbose : boolean; If True prints the progress;
    - write :  boolean, whether to save the file to data folder or not.
    - save_file_path : controls how many levels up to go to the saving directory, data; it is not a full path 

  Output
  ------ 
    - dataframe with duplicates consisting of current id, id duplicate, their titles, type and cos similarty 
     between [0, 1]; 1 meaning the resources are almost identical in terms of their vocabularily;

  """

  if verbose:
    print('\nDetecting duplicates for {} resources ... '.format(df_latest.shape[0]))
  duplicates = []

  for j, resource in tqdm(df_latest.iterrows()):

    if 'vocabulary' in locals():
      del vocabulary

    type_ = resource['res_type_id']
    text = resource['content']
    lan = resource['language_id']

    # Filter df_ref on type and language
    df_ref_lan = df_ref[(df_ref['language_id'] == lan) & (df_ref['res_type_id'] == type_)]
    id_df_ref_lan = np.array(df_ref_lan['id'])
    name_voc = save_file_path + 'data/interim/tf_voc/tf_voc_' + str(type_) + '_' + dict_lan[str(lan)] + '.json'

    # Loading the vocabulary from file, if found
    try:
      x = []
      with open(name_voc) as f:
        for i in f:
          x.append(json.loads(i))
      vocabulary = x[0]
    except:
      if verbose:
        print("")

    # Combine the text + ref resources
    documents = pd.concat([pd.Series(text), df_ref_lan['content']])

    # If vocabularily is found in /tf_voc/, detect duplicates
    if 'vocabulary' in locals():
      # Compute term frequencies 
      cv = CountVectorizer(vocabulary=vocabulary)
      tf_doc = cv.fit_transform(documents).toarray()
      # Scaling the text  
      scaler = MaxAbsScaler()
      normalizer = Normalizer()
      pipeline = make_pipeline(scaler, normalizer)
      tf_doc = pipeline.fit_transform(tf_doc)

      # Computing the similarity
      resource2recommend = np.reshape(tf_doc[0, :], tf_doc.shape[1])
      similarity_mat = np.dot(tf_doc[1:, :], np.array(resource2recommend))
      similarity_max_index = np.argmax(similarity_mat) # the position where the max value is.

      id_current = resource['id']
      id_duplicate = int(id_df_ref_lan[similarity_max_index])
      cos_similarity = similarity_mat[similarity_max_index] 

      duplicates.append({'id': id_current, 'id_dup': id_duplicate, 
                          'res_type_id': resource['res_type_id'],
                          'language_id' : lan, 
                          'cos_similarity': cos_similarity,
                          'title': resource['title'],
                          'title_dup': df_ref_lan[df_ref_lan['id'] == id_duplicate]['title'].item(),
                          'content' : text[0:100], 
                          'content_dup': df_ref_lan[df_ref_lan['id'] == id_duplicate]['content'].item()[0:100]})

  duplicates = pd.DataFrame(duplicates)
  duplicates = duplicates_post_processing(duplicates, df_dup_validated, verbose=verbose)

  fname = save_file_path + 'data/interim/duplicates_latest.csv'
  if write:
    duplicates.to_csv(path_or_buf=fname, header=True, index=False)  
    if verbose:
      print('Duplicates were written to {}.'.format(fname))

  return duplicates

if __name__ == "__main__":
  pass  