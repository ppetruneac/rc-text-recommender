 # rc-text-recommender 
  ============================== 

 This project identifies textual duplicates and recommends similar resources. 
 
 ### Identifying Duplicates
 Similar resources are identified based on [cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity). The most similar resource is returned and loaded into MySQL. 
 
 > **Assumptions**: 
 - Raw data read from source (i.e. MySQL) has language as attribute / column. 
 - There is a language dictioanry for all language id in both `detect_duplciates.py` and `get-term_frequency.py` file. This is used to load common words in one particular language. 
 - Duplicates are identified based on the vocabularily of the same resource type and language. 

 
 > **Note**: [all_duplicates.csv](data/all_duplicates.csv) contains duplicates that were previously generated and manually validated. It is recommended for these to be deleted first from the database. 
 
 **Setup**
 - install [Python](www.python.org) and ideally use a virtual environment. 
 - `pip install -r requirements.txt` to install Python package requirements.
 
 **src/functions**: change the *.sql files to accomodate the current database and tables. Do not change the relative file paths. 
 - `make_dataset_duplicates.py`: function to read reference and latest data (24h). Change SQL query if needed.
 - `load_duplicates_to_MySQL.sql`: change to load into the actual database and table
 
 **main_detect_duplicates.py** 
 - main function to run on terminal. Change the *bashCommand* to be able to execute for your user account.
 
 **How to run**
 ```
 cd src
 python3 main_detect_duplicates.py 
 ```

 
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
  
  
