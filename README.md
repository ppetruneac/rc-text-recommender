 # rc-text-recommender 
  ============================== 

 This project idenitfies textual duplicates and recommends similar resources. 
 
 ### Identifying Duplicates
 Similar resources are identified based on cosine similarity. The most similar resource is returned. 
 
 > Assumption: 
 Raw data read from source (i.e. MySQL) has language as attribute / column. If not, please use [detect_language.py](https://github.com/ppetruneac/rc-text-recommender/blob/master/src/functions/detect_language.py) in *src/functions* to detect the language, then upload the data back to MySQL. 
 
 > Note: [all_duplicates.csv](data/all_duplicates.csv) contains duplicates that were previously generated and manually validated. It is recommended for these to be deleted first from the database. 
 
 **Setup**
 - install [Python](www.python.org) and ideally use a virtual environment. 
 - `pip install -r requirements.txt` to install Python package requirements.
 
 **src/functions**: change the *.sql files to accomodate the current database and tables. Do not change the relative file paths. 
 - `create_mysql_db_test_mode.sql`: creates a database for test purpose & creates a database and table for duplicates
 - `make_dataset_duplicates.sql`: change to read from actual database and table
 - `load_duplicates_to_MySQL.sql`: change to load into the actual database and table
 
 **main_detect_duplicates.py** 
 - main function to run on terminal. Change the *bashCommand* to be able to execute.

 
 ### Recommending similar resources 
 > Nothing on this at the moment.



  
  ### Project Organization
  ------------

    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── interim        <- Intermediate data that has been transformed.
    │   └── sample         <- A sample of the original data.
    │
    ├── docs               <- Project Documentation that includes busines problem, assumtions, data wrangling & exploration, 
    │                         model methodology, development and implementation.
    │
    ├── logs               <- Logs directory
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Notebooks (i.e. 'notebook.xyz')
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── src                <- Source code for use in this project.
       ├── main.xyz        <- Main code to run. 
       │
       ├── functions       <- Scripts to download/generate data; build features, train models or visualize data. 
          |
          └── make_dataset.xyz
          └── build_features.xyz
          └── train.xyz
          └── visualize.xyz

   Project structure inspired by [cookiecutter](https://cookiecutter.readthedocs.io/en/latest/).
  
  
