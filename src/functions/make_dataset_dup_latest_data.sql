-- This file will read a sample of the data from MySQL.
-- file will connect to db and create csv file in sample/data/dataset_duplicates_latest.csv

use resurse_crestine;

SELECT *
FROM resurse 
ORDER BY RAND() LIMIT 100
INTO OUTFILE '/tmp/dataset_duplicates_latest.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
