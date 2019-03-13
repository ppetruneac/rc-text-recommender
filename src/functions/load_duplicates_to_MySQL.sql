
use duplicates;
LOAD DATA LOCAL INFILE '../data/interim/duplicates_latest.csv' 
INTO TABLE duplicates.duplicates
  FIELDS TERMINATED BY ','
  LINES TERMINATED BY '\n'
  IGNORE 1 ROWS;