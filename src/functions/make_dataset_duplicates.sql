-- This section will read ALL the data from MySQL, apart from new resources (latest data, presumably last day)
-- where you specify in WHERE clause.
-- file will be saved in the /tmp/, then moved to sample/data/dataset_duplicates_all.csv
use resursenew;

SELECT
  resources.id,
  resources.res_type_id,
  resources.language_id,
  resources.title,
  resources.created_at,
  text_details.content  
FROM
  resources
LEFT JOIN text_details ON resources.id = text_details.resources_id
WHERE
  text_details.content is not null and resources.created_at < (NOW() - INTERVAL 300 HOUR) -- resources not in the last 24h.  
INTO OUTFILE '/tmp/dataset_duplicates_all.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';


-- This section will read a sample of the data from MySQL (i.e. last day).
-- file will be saved in the /tmp/, then moved to sample/data/dataset_duplicates_latest.csv
use resursenew;

SELECT
  resources.id,
  resources.res_type_id,
  resources.language_id,
  resources.title,
  resources.created_at,
  text_details.content  
FROM
  resources
LEFT JOIN text_details ON resources.id = text_details.resources_id
WHERE
  text_details.content is not null and resources.created_at > (NOW() - INTERVAL 300 HOUR) -- resources not in the last 24h.  
INTO OUTFILE '/tmp/dataset_duplicates_latest.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
