
import json, swifter, warnings
import numpy as np
import pandas as pd

from langdetect import detect

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import MaxAbsScaler, Normalizer
from sklearn.pipeline import make_pipeline

# import clean_data
warnings.simplefilter("ignore")


def detect_duplicates(df_ref, df_latest, verbose=True, write = True, save_file_path = "../../"):
  """
  This function is being used to detect duplicates, or to generate the most similar resource to a given resource.
  The aim of this function is to be used in real time when the users upload resources.

  Assumption: It is assumed that resources of the same type are duplicates.  

  Input: 
    - type_: this is the resource type as string, presumably chosen from a drop-down list; 
    - text: this is the resource the user uploads; 
    - verbose: boolean; If True prints the progress;
    - write =  boolean, whether to save the file to data folder or not.
    - save_file_path: controls how many levels up to go to the saving directory, data; it is not a full path 

  Output: 
    - dataframe with duplicates conssiting of icurrent id, id duplicates, and cos similarty 
     between [0, 1] - 1 meaning the resources are duplicates;

  """

# verbose = True
# df_ref = pd.read_csv('../../data/sample/tilda_separated.csv', delimiter='~')
# df_latest = pd.read_csv('../../data/sample/dataset_duplicates_latest.csv')
# df_latest.columns = ['id', 'title', 'type', 'content', 'datetime']
# df_latest = df_latest[['id', 'title', 'type', 'content']]
# # Cleaning the data
# df_ref = clean_data.clean_data(df_ref, verbose = True, write = False, save_file_path = "../")
# df_latest = clean_data.clean_data(df_latest, verbose = True, write = False, save_file_path = "../")
# # Only for testing mode -- DELETE when read from actual MySQL.
# # This will remove the latest resources (id level) from the all data. 
# df_ref = df_ref[~df_ref['id'].isin(df_latest.id)]

  if verbose:
    print('\nDetecting duplicates ... ')
  types = df_latest['type'].unique()
  n_duplicates = 3
  duplicates = []

  # Itenitfy duplicates for each type
  for i, type_ in enumerate(types):
    # type_ = types[0]

    if verbose:
      print("\nWorking on type {} out of {} ... ".format(type_, len(types)))
    df_ref_type_ = df_ref[df_ref.type == type_]
    df_latest_type_ = df_latest[df_latest.type == type_]

    if verbose:
      print('\tDetecting the language ... ')

    # Detecting the language for both df
    language = df_ref_type_['content'].swifter.progress_bar(False).apply(lambda x: detect(x) if x != None else np.nan)
    df_ref_type_.loc[df_ref_type_.index.values, 'language'] = np.array(language)

    language = df_latest_type_['content'].swifter.progress_bar(False).apply(lambda x: detect(x) if x != None else np.nan)
    df_latest_type_.loc[df_latest_type_.index.values, 'language'] = np.array(language)
    language = df_latest_type_['language'].value_counts()

    if verbose:
      print("\tThere are {} languages.".format(len(language)))

    # Itenitfy duplicates for each language
    for i, lan in enumerate(language.index.values):
      # lan = language.index.values[0]
      if verbose:
        print("\t\tWorking on language: {}".format(lan))

      df_ref_lan = df_ref_type_[df_ref_type_['language'] == lan]
      df_latest_lan = df_latest_type_[df_latest_type_['language'] == lan]

      if verbose:
        print("\t\t\t{} new resources; {} resources as ref in MySQL..."\
          .format(df_latest_lan.shape[0], df_ref_lan.shape[0]))

      # Reading the vocabulary
      name_voc = save_file_path + 'data/interim/tf_voc/tf_voc_' + str(type_) + '_' + lan + '.json'

      try:
        # Loading the vocabulary from file
        x = []
        with open(name_voc) as f:
          for i in f:
            x.append(json.loads(i))
        vocabulary = x[0]
      except:
        if verbose:
            print("\t\t\tNot enough resources for this language ... ")

      if 'vocabulary' in locals():
        if verbose:
            print("\t\t\tComputing term frequencies ... ")

        id_df_latest_lan = df_latest_lan['id'].values
        df_combined = pd.concat([df_ref_lan, df_latest_lan], axis = 0)
        id_df_combined = df_combined['id'].values

        cv = CountVectorizer(vocabulary=vocabulary)
        tf_doc = cv.fit_transform(df_combined['content']).toarray()

        # Scaling the text  
        scaler = MaxAbsScaler()
        normalizer = Normalizer()
        pipeline = make_pipeline(scaler, normalizer)
        tf_doc = pipeline.fit_transform(tf_doc)

        if verbose:
            print("\t\t\tDetecting duplicates ... ")

        # For every id in the new dataframe, detect duplicates. 
        for id in id_df_latest_lan:
          # i = 0
          # id = id_df_latest_lan[i]
          # Get the tf of the resource to recommend
          id_resource2recommend = np.where(id_df_combined == id)
          resource2recommend = tf_doc[id_resource2recommend, :]
          resource2recommend = np.reshape(tf_doc[0, :], tf_doc.shape[1])

          # Remove the resource to recommend from the whole data: tf_doc
          # Remove the id of resource to recommend from id_df_combined
          tf_doc_new = np.delete(tf_doc, id_resource2recommend, axis = 0)
          id_df_combined_new = np.delete(id_df_combined, id_resource2recommend) 
          
          cos_similarity_mat = np.dot(tf_doc_new, resource2recommend)
          similarity_max_index = np.argmax(cos_similarity_mat)

          id_duplicate = id_df_combined_new[similarity_max_index]
          cos_similarity = cos_similarity_mat[similarity_max_index]

          duplicates.append( {'id': id, 'index_duplicate': id_duplicate, 'cos_similarity': cos_similarity})

        del vocabulary

  if write:
    duplicates = pd.DataFrame(duplicates) 
    fname_duplicates = save_file_path + 'data/interim/duplicates_latest.csv'
    duplicates.to_csv(fname_duplicates, header=None, index=False)

    if verbose:
      print("Duplicates were written to {}.".format(fname_duplicates))
      print('Finished detecting duplicates!')

  # df_combined[df_combined.id.isin([id, index_duplicate])]

  return duplicates 


# dict_type = {'Acorduri': 1, 'Cântece': 2, 'Devoționale': 3, 'Editoriale': 4, 'Eseuri': 5, 'Maxime': 6, \
#             'Poezii': 7, 'Schițe': 8, 'Studii': 9, 'Predici': 10, 'Cărți': 11, 'Scenete': 12, \
#             'Powerpoint': 13, 'Reviste': 14, 'Partituri': 15, 'Biblia': 16, 'Jocuri': 37, 'Lecția zilnică': 39, \
#             'Versete': 41, 'Biografii': 42, 'Mărturii': 43, 'Programe creștine': 45, 'Cugetări': 46, 'Dezbateri':47}

# type_ = 1
# dict_type = {'1': 'Acorduri', '2': 'Cântece'}
# dict_type[str(type_)]