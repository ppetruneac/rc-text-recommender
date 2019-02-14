
-- This script creates a db and writes a sample table;

SET GLOBAL local_infile = 1;
set global max_allowed_packet = 1000000;

CREATE DATABASE resurse_crestine;
use resurse_crestine;

CREATE TABLE resurse (id INT NOT NULL, 
  title VARCHAR(500) NOT NULL, 
  type INT NOT NULL, 
  content TEXT,
  datetime DATETIME,  
  PRIMARY KEY (id));

LOAD DATA LOCAL INFILE '../data/sample/tilda_separated_filter_clean.csv' 
INTO TABLE resurse_crestine.resurse
  FIELDS TERMINATED BY ','
  LINES TERMINATED BY '\n'
  IGNORE 1 ROWS;







