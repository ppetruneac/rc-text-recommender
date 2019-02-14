-- This file will read ALL the data from MySQL.
-- file will connect to db and create csv file in sample/data/tilda_separated_first_run.csv

use resurse_crestine;

SELECT *
FROM resurse LIMIT 10
INTO OUTFILE '../../data/sample/tilda_separated_first_run.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';



