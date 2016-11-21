import mysql.connector
import time
import json

from mysql.connector import Error

def insertTweetToMySql(data):
  try:
        conn = mysql.connector.connect(host='localhost',
                                       database='nlptext',
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

              datum["user"]["description"] = datum["user"]["description"].replace("'","")
              cursor.execute("INSERT INTO twitter (created_at,teks, name, location, description, follower_count, friends_count, retweet_count) VALUES (\'" + datum["created_at"] + "\',\'" + (datum["text"]) + "\',\'" + datum["user"]["name"] + "\',\'" + (datum["user"]["location"]) + "\',\'" + (datum["user"]["description"]) + "\'," + str(datum["user"]["followers_count"]) + "," +str(datum["user"]["friends_count"]) + "," + str(datum["retweet_count"]) + ")")
              conn.commit()
            print("Finish add to database")
  except Error as e:
    print(e)

if __name__ == '__main__':
  with open('dataahok.json') as data_file:
    data = json.load(data_file)
  insertTweetToMySql(data)