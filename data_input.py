import database_lib as db
import mysql.connector
from mysql.connector import errorcode


cnx = mysql.connector.connect (
      user = 'root',
      host = 'localhost',
      password = 'root',
)

DB_NAME = 'game_companies'
cursor = cnx.cursor()

db.create_db(cursor, DB_NAME)
cursor.execute(f"USE {DB_NAME}")
db.initialization(cursor)
cnx.commit()    
    
