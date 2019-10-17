# Script to run detect duplicates on bash + insert data into MySQL

while getopts u:d:p:f: option
do
case "${option}"
in
u) USER=${OPTARG};;
p) PASSWORD=${OPTARG};;
esac
done

# run the detect duplicates
python main_detect_duplicates.py -u $USER -p $PASSWORD

echo "\n"
echo 'Loading the latest duplicates to MySQL ...'

# Insert the latest_duplicates.csv file in MySQL
mysql -u $USER -p$PASSWORD  -e "LOAD DATA LOCAL INFILE '/root/rc-text-recommender/data/interim/duplicates_latest.csv' 
INTO TABLE resursenew.duplicates_detected
  FIELDS TERMINATED BY ','
  LINES TERMINATED BY '\n'
  IGNORE 1 ROWS;"
