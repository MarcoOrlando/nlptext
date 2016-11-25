import mysql.connector
import time
import json

from mysql.connector import Error

def insertTweetToMySql(data, calon):
  try:
        conn = mysql.connector.connect(host='localhost',
                                       database='nlp_text',
                                       user='root',
                                       password='')


        if conn.is_connected():
            cursor = conn.cursor();
            print('Connected to MySQL database')

            for datum in data:
              datum["text"] = datum["text"].replace("'", "")
              datum["user"]["name"] = datum["user"]["name"].replace("'","")
              if (datum["user"]["location"] is None):
                datum["user"]["location"] = 'UNKNOWN'

              if (datum["user"]["description"] is None):
                datum["user"]["description"] = 'UNKNOWN'

              datum["user"]["location"] = datum["user"]["location"].replace("'","")

              datum["user"]["description"] = datum["user"]["description"].replace("'","")

              if 'retweeted_status' in datum:
                datum['retweet_count'] = datum['retweeted_status']['retweet_count']

              cursor.execute("INSERT INTO twitter (created_at,teks, name, location, description, follower_count, friends_count, retweet_count, calon, tweet_id) VALUES (\'" + datum["created_at"] + "\',\'" + (datum["text"]) + "\',\'" + datum["user"]["name"] + "\',\'" + (datum["user"]["location"]) + "\',\'" + (datum["user"]["description"]) + "\'," + str(datum["user"]["followers_count"]) + "," +str(datum["user"]["friends_count"]) + "," + str(datum["retweet_count"]) + ",\'" + calon + "\',\'" + str(datum["id"]) + "\')")
              conn.commit()
            print("Finish add to database")
        conn.close()
  except Error as e:
    print(e)

def insertTweetKata(data, calon):
  #0 : tweet_id
  #1 : kata
  try:
        conn = mysql.connector.connect(host='localhost',
                                       database='nlp_text',
                                       user='root',
                                       password='')
        if conn.is_connected():
            cursor = conn.cursor();
            print('Connected to MySQL database')

            for datum in data:
              cursor.execute("INSERT INTO tweet_kata (calon, kata, tweet_id) VALUES (" + calon + "\',\'" + datum[1] + "\',\'" + datum[0] + "\')")
              conn.commit()
            print("Finish add to database")
        conn.close()
  except Error as e:
    print(e)

def insertTweetResult(data, calon):
  #0 : kata
  #1 : jumlah_kemunculan
  try:
        conn = mysql.connector.connect(host='localhost',
                                       database='nlp_text',
                                       user='root',
                                       password='')
        if conn.is_connected():
            cursor = conn.cursor();
            print('Connected to MySQL database')

            for datum in data:
              cursor.execute("INSERT INTO tweet_result (calon, kata, jumlah_kemunculan) VALUES (" + calon + "\',\'" + datum[0] + "\'," + str(datum[1]) + ")")
              conn.commit()
            print("Finish add to database")
        conn.close()
  except Error as e:
    print(e)


if __name__ == '__main__':
  with open('dataanies.json') as data_file:
    data = json.load(data_file)

  insertTweetToMySql(data, "ANIES")