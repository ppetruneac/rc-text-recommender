# Script to run detect duplicates on bash + insert data into MySQL
# How to run: bash main_duplicates.sh -u <USER> -p <PASSWORD>

while getopts u:d:p:f: option
do
case "${option}"
in
u) USER=${OPTARG};;
p) PASSWORD=${OPTARG};;
esac
done

# run the detect duplicates
cd /root/rc-text-recommender/detect_duplicates
python3 main_detect_duplicates.py -u $USER -p $PASSWORD

echo 'Loading the latest duplicates to MySQL ...'

# Insert the latest_duplicates.csv file in MySQL
mysql -u $USER -p$PASSWORD  -e "LOAD DATA LOCAL INFILE '/root/rc-text-recommender/data/interim/duplicates_latest.csv' 
INTO TABLE resursenew.duplicates_to_validate
  FIELDS TERMINATED BY ','
  LINES TERMINATED BY '\n'
  IGNORE 1 ROWS;"

echo 'DONE! '