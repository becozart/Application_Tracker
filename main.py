# https://dev.mysql.com/doc/connector-python/en/

import mysql.connector
from mysql.connector import errorcode

try:
    cnx = mysql.connector.connect(option_files="config.ini")
except mysql.connector.Error as e:
    if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Incorrect Username or Password.")
    elif e.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist.")
    else:
        print(e)
else:
    cnx.close()

print(cnx)

cnx.close()
