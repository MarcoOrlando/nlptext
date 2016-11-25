import mysql.connector
import json

from mysql.connector import Error

def insertTweetResult(data, calon):
  #0 : kata
  #2 : jumlah_kemunculan
  try:
        conn = mysql.connector.connect(host='localhost',
                                       database='nlp_text',
                                       user='root',
                                       password='')
        if conn.is_connected():
            cursor = conn.cursor();
            print('Connected to MySQL database')

            for datum in data:
              cursor.execute("INSERT INTO tweet_result (calon, kata, jumlah_kemunculan) VALUES (\'" + calon + "\',\'" + datum[0] + "\'," + str(datum[1]) + ")")
              conn.commit()
            print("Finish add to database")
        conn.close()
  except Error as e:
    print(e)


if __name__ == "__main__":
  filename = 'ahy_result_saved.txt'
  data = []
  with open(filename, 'r') as the_file:
    for line in the_file:
      word = line.split(',')
      word[1].replace('/n','')
      word2 = (word[0],int(word[1]))
      data.append(word2)
  insertTweetResult(data, "AHY")
