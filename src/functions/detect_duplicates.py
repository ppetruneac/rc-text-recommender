
import json, swifter, warnings
import numpy as np
import pandas as pd

from langdetect import detect
from tqdm import tqdm

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import MaxAbsScaler, Normalizer
from sklearn.pipeline import make_pipeline

warnings.simplefilter("ignore")


def detect_duplicates(df_ref, df_latest, verbose=True, write = True, save_file_path = "../../"):
  """
  
  This function is being used to detect duplicates, or to generate the most similar resource to a given resource.

  Assumptions
  -----------
    - df_ref and df_latest will be clean before feeding into this function.  

  Parameters
  ---------- 
    - df_ref : dataframe with all resources; with columns [id, title, type, content]
    - df_latest : dataframe with latest resources to detect duplicates; with columns [id, title, type, content]
    - verbose : boolean; If True prints the progress;
    - write :  boolean, whether to save the file to data folder or not.
    - save_file_path : controls how many levels up to go to the saving directory, data; it is not a full path 

  Output
  ------ 
    - dataframe with duplicates consisting of current id, id duplicate, their titles, type and cos similarty 
     between [0, 1] - 1 meaning the resources are almost identical in terms of theor vocabularily;

  """


  if verbose:
    print('\nDetecting duplicates for {} resources ... '.format(df_latest.shape[0]))
  duplicates = []


  for j, resource in tqdm(df_latest.iterrows()):

    if 'vocabulary' in locals():
      del vocabulary

    type_ = resource['type']
    text = resource['content']
    lan = detect(text)

    # Filter or type and language
    df_ref_lan = df_ref[(df_ref['language'] == lan) & (df_ref['type'] == type_)]
    id_df_ref_lan = np.array(df_ref_lan['id'])
    name_voc = save_file_path + 'data/interim/tf_voc/tf_voc_' + str(type_) + '_' + lan + '.json'

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
      similarity_max_index = np.argmax(similarity_mat)

      id_current = resource['id']
      id_duplicate = int(id_df_ref_lan[similarity_max_index])
      cos_similarity = similarity_mat[similarity_max_index] 

      duplicates.append( {'id': id_current, 'id_dup': id_duplicate, 
                          'type': resource['type'],
                          'cos_similarity': cos_similarity,
                        'title': resource['title'],
                        'title_dup': df_ref_lan[df_ref_lan['id'] == id_duplicate]['title'].item()})

  duplicates = pd.DataFrame(duplicates)
  duplicates = duplicates[['id', 'id_dup', 'title', 'title_dup', 'cos_similarity', 'type']]
  fname = save_file_path + 'data/interim/duplicates_latest.csv'

  if write:
    duplicates.to_csv(path_or_buf=fname, header=True, index=False)  
    if verbose:
      print('Duplicates were written to {}.'.format(fname))

  return duplicates