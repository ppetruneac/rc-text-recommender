 # rc-text-recommender 
  ============================== 

 This project identifies textual duplicates and recommends similar resources. 
 
 ### Identifying Duplicates
 Similar resources are identified based on [cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity). The most similar resource is returned and loaded into MySQL. 
 
 > **Assumptions**: 
 - Raw data read from source (i.e. MySQL) has language as attribute / column. 
 - There is a language dictioanry for all language id in both `detect_duplciates.py` and `get-term_frequency.py` file. This is used to load common words in one particular language. 
 - Duplicates are identified based on the vocabularily of the same resource type and language. 

 
 > **Note**: [all_duplicates.csv](data/all_duplicates.csv) contains duplicates that were previously generated and manually validated. This needs to be uploaded into a database/table (i.e. *duplicates.all_duplicates*)
 
 **Setup**
 - install [Python](www.python.org) and ideally use a virtual environment. 
 - `pip install -r requirements.txt` to install Python package requirements.
 
 **src/functions**: Do not change the relative file paths. 
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


 
