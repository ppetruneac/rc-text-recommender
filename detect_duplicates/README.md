

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

  > **Note**: [data/all_duplicates.csv](data/all_duplicates.csv) contains duplicates that were previously generated and manually validated. 
  This file was uploaded in MySQL `resursenew` database with table `duplicates_detected` (see Appendix query 1 for help).

  
 ## Instructions 
 - run `bash ../requirements.sh` to install dependancies from fresh in CentOS
 
 Otherwise:

- install [Python 3](www.python.org) and ideally use a virtual environment. 
- `pip install -r requirements.txt` to install Python package requirements.


**Files:**

- [main_detect_duplicates.py](main_detect_duplicates.py) -- main function to run on terminal. This will save the duplicates data in the data/interim folder in *csv* format. Change the *bashCommand* to be able to execute for your user account.  
- [load_duplicates_to_MySQL.sql](load_duplicates_to_MySQL.sql) can be used to laod the duplicates data into `duplicates.duplicates_detected` table in MySQL. --> **NEEDS TO BE APPENDED / UNION.** Once this is working, can uncomment last lines of code in [main_detect_duplicates.py](./main_detect_duplicates.py#63)
- the other files are used in the [main_detect_duplicates.py](main_detect_duplicates.py)
 
 
 
 **How to run**
 ```
 cd detect_duplicates
 python3 main_detect_duplicates.py 
 ```

 ## Appendix

 Query 1: load `all_duplicates.csv` data in MySQL:

 ```
 create database IF NOT EXISTS duplicates;

CREATE TABLE IF NOT EXISTS resursenew.duplicates_detected
(
  id                  INT NOT NULL,  
  id_dup              INT NOT NULL,                 
  res_type_id         INT NOT NULL,                 
  language_id         INT NOT NULL,                 
  title               text,
  title_dup           text,
  content             text,
  content_dup         text,
  cos_similarity      double,
  content_distance    double,
  title_distance      double,
  certainty           text                       
);

LOAD DATA LOCAL INFILE '/root/rc-text-recommender/data/all_duplicates.csv' 
INTO TABLE resursenew.duplicates_detected
  FIELDS TERMINATED BY ','
  LINES TERMINATED BY '\n'
  IGNORE 1 ROWS;
 ```
