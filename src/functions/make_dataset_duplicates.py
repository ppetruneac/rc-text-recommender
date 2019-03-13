import pymysql
import pandas as pd


def read_data(host, user, password, db):

  """
  Function that reads data from MySQL and returns 2 data frames: one with all data but not the last X (24 hours)
  and the 2nd one containing data in the last X (24) hours.

  Arguments:
  ----------
  host : your host, usually localhost
  user : your username
  passwd : your password
  db : database name to be used

  Output:
  -------
  df_ref and df_latest : df containing reference and latest data. 
  """

  connection = pymysql.connect(host=host, user=user, passwd=password,db=db) 
  cursor = connection.cursor()

  query_ref = """
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
    text_details.content is not null and resources.created_at < (NOW() - INTERVAL 24 HOUR)
  """
  df_ref = pd.read_sql(query_ref, connection)

  query_latest = """
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
    text_details.content is not null and resources.created_at > (NOW() - INTERVAL 24 HOUR) -- resources not in the last 24h.  
    """

  df_latest = pd.read_sql(query_latest, connection)

  connection.close()

  return df_ref, df_latest

if __name__ == "__main__":
    pass  