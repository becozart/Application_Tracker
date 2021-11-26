# https://dev.mysql.com/doc/connector-python/en/

import mysql.connector
from mysql.connector import errorcode


def main():

    db_name = 'applications'

    tables = {}
    tables['applications'] = (
        "CREATE TABLE `applications` ("
        "  `app_no` int(11) NOT NULL AUTO_INCREMENT,"
        "  `company_name` varchar(40) NOT NULL,"
        "  `position_name` varchar(40) NOT NULL,"
        "  `date_applied` date NOT NULL,"
        "  `result` varchar(15),"
        "  `source` varchar(20) NOT NULL,"
        "  `link` varchar(200),"
        "  `notes` varchar(200),"
        "  PRIMARY KEY (`app_no`)"
        ") ENGINE=InnoDB")

    try:
        cnx = mysql.connector.connect(option_files="config.ini")
        cursor = cnx.cursor()
    except mysql.connector.Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Incorrect Username or Password.")
        elif e.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
        else:
            print(e)

    try:
        cursor.execute("USE {}".format(db_name))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(db_name))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor, db_name)
            print("Database {} created successfully.".format(db_name))
            cnx.database = db_name
        else:
            print(err)
            exit(1)

    for table_name in tables:
        table_description = tables[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    # while True:
    #     print("What would you like to do?")
    #     input()

    cursor.close()
    cnx.close()


def create_database(cursor, db_name):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


if __name__ == "__main__":
    main()