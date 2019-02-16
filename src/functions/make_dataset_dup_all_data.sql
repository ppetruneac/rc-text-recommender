-- This file will read ALL the data from MySQL, apart from new resources (latest data).
-- file will connect to db and create csv file in sample/data/dataset_duplicates_all.csv

use resurse_crestine;

SELECT *
FROM resurse -- WHERE date not in last day 
INTO OUTFILE '/tmp/dataset_duplicates_all.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';