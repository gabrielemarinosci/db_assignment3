import database_lib as db
import mysql.connector
from mysql.connector import errorcode


cnx = mysql.connector.connect(
    host = "localhost",\
    port = "3307",
    user = "root",
    passwd = "root",
    unix_socket= '/Applications/MAMP/tmp/mysql/mysql.sock',
)

DB_NAME = 'game_companies'
cursor = cnx.cursor()

#db.create_db(cursor, DB_NAME)
cursor.execute(f"USE {DB_NAME}")
#db.initialization(cursor)
#cnx.commit()   
db.ceo_of_the_company_who_made_game(cursor) 