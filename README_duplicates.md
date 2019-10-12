

 # Identifying Duplicates 

 This branch focuses on identifying duplicates in text based data such as lyrics and poems. Duplicate resources are largely identified based on [cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity) and identified based on the vocabularily of the same resource type and language.

**Assumptions**
- assumes that duplicates are desired to be found for resources that have been uploaded in the last x hours. 
- focuses on only text type data and for types with at least x number of observation by language. 

The above can be deifned in [src/main_detect_duplicates.py](src/main_detect_duplicates.py). 

 
 ## Data

 Data came in *.sql* format and it was an extraction of the actual MySQL database. The file was imported in MySQL Workbench locally in *resursenew*. The tables are: `resources`, `res_type` and `text_details`. 

 Plese refer to [docs/data_overview.ipynb](docs/data_overview.ipynb) for details on the exact fields in the raw dataset. 

  > **Note**: [data/all_duplicates.csv](data/all_duplicates.csv) contains duplicates that were previously generated and manually validated. This file was uploaded in MySQL `duplicates` database with tables `all_duplicates` and `all_duplicates_modelled` (added column *certainty* if the duplicates were validated). 

  
 **Setup**
 - install [Python](www.python.org) and ideally use a virtual environment. 
 - `pip install -r requirements.txt` to install Python package requirements.

 **main_detect_duplicates.py** 
 - main function to run on terminal. Change the *bashCommand* to be able to execute for your user account.
 
 **src/functions**: 
 - `load_duplicates_to_MySQL.sql`: change to load into the actual database and table
  
 
 **How to run**
 ```
 cd src
 python3 main_detect_duplicates.py 
 ```


  
  ## Project Organization
  

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
  
  
