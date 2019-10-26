# This script needs to be run once, at the beginning. It does 2 things: 
# 1. Creates table and it loads data into: resursenew.duplicates_validated
# 2. Creates the table: resursenew.duplicates_to_validate

while getopts u:d:p:f: option
do
case "${option}"
in
u) USER=${OPTARG};;
p) PASSWORD=${OPTARG};;
esac
done

# 1. Creates table and it loads data into: resursenew.duplicates_validated
mysql -u $USER -p$PASSWORD  -e "CREATE TABLE IF NOT EXISTS resursenew.duplicates_validated
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
INTO TABLE resursenew.duplicates_validated
  FIELDS TERMINATED BY ','
  LINES TERMINATED BY '\n'
  IGNORE 1 ROWS;"

# 2. Creates the table: resursenew.duplicates_to_validate
mysql -u $USER -p$PASSWORD  -e "CREATE TABLE IF NOT EXISTS resursenew.duplicates_to_validate
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
); "