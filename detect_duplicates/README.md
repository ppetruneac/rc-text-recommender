

 # Identifying Duplicates 

 This folder focuses on identifying duplicates in text based data such as lyrics and poems. Duplicate resources are largely identified based on [cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity) and identified based on the vocabularily of the same resource type and language.

**Assumptions**
- assumes that duplicates are desired to be found for text resources that have been uploaded on the website in the last {x} hours. 
- assumes that older duplicates have been dealt with before
- focuses on only text type data and for types with at least {x} number of observation by language.  

The above {parameters} can be defined in [config.yaml](./config.yaml). 

 ## Data

 Data came in *.sql* format and it was an extraction of the actual MySQL database. The file was imported in MySQL Workbench locally in *resursenew*. The tables are: `resources`, `res_type` and `text_details`. 

 Plese refer to [docs/data_overview.ipynb](docs/data_overview.ipynb) for details on the exact fields in the raw dataset. 

 ## Instructions 
 - run `bash requirements.sh` to install dependancies from fresh in CentOS. This installs Python + dependant packages. 
 - run (ONLY for the first time): `bash initialisation_mysql.sh  -u <USER> -p <PASSWORD>` to create some MySQL tables and load some data in (i.e. `duplicates_validated` in `duplicates_validated` table). 
 

**Files:**
- [utils.py](utils.py): utility functions
- [detect_duplicates.py](detect_duplicates.py): core code for detecting duplicates
- [main_detect_duplicates.py](main_detect_duplicates.py) -- main function to run on terminal. This will save the duplicates data in the data/interim folder in *csv* format. 
- [main_detect_duplicates.sh](main_detect_duplicates.sh): main file to run on bash. It runs [main_detect_duplicates.py](main_detect_duplicates.py) and then it loads the results into MySQL. 
 
 
 
 **How to run**
 ```
 bash main_duplicates.sh -u <USER> -p <PASSWORD>
 ```
 