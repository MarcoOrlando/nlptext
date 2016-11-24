




try:
      conn = mysql.connector.connect(host='localhost',
                                     database='pilkada',
                                     user='root',
                                     password='')
      if conn.is_connected():
          cursor = conn.cursor();
          print('Connected to MySQL database')
          with open("../ahok_result.txt", "r") as hasil:
            lines = hasil.readlines()

            for line in lines:
                # Split the line on whitespace
                data = line.split(",")
                kata = data[0]
                jumlah = data[1]

            # Put this through to SQL using an INSERT statement...
                cursor.execute("""INSERT INTO tweet_kata (calon, kata, tweet_id)
                           VALUES(%s, %s, %s)""", (ahok, kata, jumlah))

          print("Finish add to database")
      conn.close()
