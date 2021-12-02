# https://dev.mysql.com/doc/connector-python/en/

import mysql.connector
from mysql.connector import errorcode
from user_interface import Ui


def __create_table_dictionary():
    tables = {'applications': (
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
        ") ENGINE=InnoDB")}

    return tables


def __create_connection(option_files):
    try:
        cnx = mysql.connector.connect(option_files=option_files)
    except mysql.connector.Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Incorrect Username or Password.")
        elif e.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
        else:
            print(e)

    return cnx


def __create_cursor(cnx):
    try:
        cursor = cnx.cursor(buffered=True)
    except mysql.connector.Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Incorrect Username or Password.")
        elif e.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
        else:
            print(e)

    return cursor


def __create_database(cnx, cursor, db_name):
    try:
        cursor.execute("USE {}".format(db_name))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(db_name))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            __create_database_helper(cursor, db_name)
            print("Database {} created successfully.".format(db_name))
            cnx.database = db_name
        else:
            print(err)
            exit(1)


def __create_database_helper(cursor, db_name):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


def __create_tables(cursor, tables):
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

    print()


def main():
    db_name = 'applications'
    tables = __create_table_dictionary()
    cnx = __create_connection("config.ini")
    cursor = __create_cursor(cnx)

    __create_database(cnx, cursor, db_name)
    __create_tables(cursor, tables)

    Ui.run(cnx, cursor)


if __name__ == "__main__":
    main()
