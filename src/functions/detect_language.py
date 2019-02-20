import pandas as pd
import numpy as np
from langdetect import detect
from tqdm import tqdm
import swifter

def detect_language(df, verbose = False):
    
    """
    Function to detect language.
    
    Assumtpion: input data will be clean from html tags etc. 
    
    Arguments
    ---------
    
    df : pd.Series
    verbose : boolean, if True uses tqdm to show the progress
    """

    if type(df) == pd.core.series.Series:    
      language = df.swifter.progress_bar(verbose).apply(lambda x: detect(x) if x != None else np.nan)
    else
      try:
        df = pd.Series(df)
        language = df.swifter.progress_bar(verbose).apply(lambda x: detect(x) if x != None else np.nan)
      except:
        TypeError('The data df provided cannot be converted to pd Series.')

    return language
