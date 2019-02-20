-- This section will read ALL the data from MySQL, apart from new resources (latest data)
-- where you specify in WHERE clause.
-- file will be saved in sample/data/dataset_duplicates_all.csv

use resurse_crestine;

SELECT id, title, type, content, language
FROM resurse -- WHERE date not in last day 
INTO OUTFILE '/tmp/dataset_duplicates_all.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';


-- This section will read a sample of the data from MySQL.
-- file will be saved in sample/data/dataset_duplicates_latest.csv

use resurse_crestine;

SELECT id, title, type, content, language
FROM resurse 
ORDER BY RAND() LIMIT 10
INTO OUTFILE '/tmp/dataset_duplicates_latest.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
