

SET GLOBAL local_infile = 1;
set global max_allowed_packet = 1000000;

-- create resurse_crestine db
drop database resurse_crestine;
CREATE DATABASE resurse_crestine;
use resurse_crestine;

CREATE TABLE resurse (id INT NOT NULL, 
  title VARCHAR(500) NOT NULL, 
  type INT NOT NULL, 
  content TEXT,
  datetime DATETIME,  
  language VARCHAR(100),
  PRIMARY KEY (id));

LOAD DATA LOCAL INFILE '../data/sample/sample_data_lan.csv' 
INTO TABLE resurse_crestine.resurse
  FIELDS TERMINATED BY ','
  LINES TERMINATED BY '\n'
  IGNORE 1 ROWS;

-- create duplicates db
drop database duplicates;
CREATE DATABASE duplicates;
use duplicates;

CREATE TABLE duplicates (id INT NOT NULL, 
  id_dup INT NOT NULL, 
  title VARCHAR(500) NOT NULL, 
  title_dup VARCHAR(500) NOT NULL, 
  cos_similarity FLOAT NOT NULL,
  type INT NOT NULL,
  PRIMARY KEY (id));



