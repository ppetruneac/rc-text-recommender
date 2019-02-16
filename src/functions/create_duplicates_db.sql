
-- This script creates a db;

SET GLOBAL local_infile = 1;
set global max_allowed_packet = 1000000;

CREATE DATABASE duplicates;
use duplicates;

CREATE TABLE duplicates ( 
  cos_similarity FLOAT NOT NULL, 
  id INT NOT NULL,
  id_duplicate INT NOT NULL, 
  PRIMARY KEY (id));