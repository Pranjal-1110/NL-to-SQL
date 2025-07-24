import mysql.connector


def get_connection():
   conn = mysql.connector.connect(
               host = "localhost",
               user = "root",
               password = "pranjal123",
               database = "bike_store"
      )
   return conn , conn.cursor()
