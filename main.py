# https://dev.mysql.com/doc/connector-python/en/

import mysql.connector
from mysql.connector import errorcode


def main():
    db_name = 'applications'
    tables = __create_table_dictionary()
    cnx = __create_connection("config.ini")
    cursor = __create_cursor(cnx)

    __create_database(cnx, cursor, db_name)
    __create_tables(cursor, tables)
    print()

    while True:
        print("Welcome to the Application Tracker!")
        print("Would you like to use SQL to work with your application data or not?")
        user_input = input("Please enter \"S\" for SQL or \"N\" for without SQL "
                           "(\"E\" to exit): ")
        print()

        if user_input.lower().strip() == "s":
            print("Welcome to the SQL side!")
            while True:
                query = input("Please enter a SQL query "
                              "(\"E\" to exit to the main menu): ")

                if query.lower().strip() == "e":
                    print()
                    break
                else:
                    cursor.execute(query)

                    for (row) in cursor:
                        print(row)

                    print("Queried")
                    print()
        elif user_input.lower().strip() == "n":
            print("Welcome to the sans-SQL side!")
            while True:
                print("Please choose on of the following options:")
                print("1: See all applications")
                print("2: Add an application")
                print("(\"E\" to exit to the main menu)")
                user_input = input("")

                if user_input.strip() == "1":
                    query = "SELECT * FROM applications"

                    cursor.execute(query)

                    for (row) in cursor:
                        print(row)

                    print()
                elif user_input.strip() == "2":
                    print("Please enter the following (Enter Null if you do not know the value):")
                    company_name = input("Company Name: ").strip()
                    position_name = input("Position Name: ").strip()
                    month_applied = input("Month Applied (2 digits): ").strip()
                    day_applied = input("Day Applied (2 digits): ").strip()
                    year_applied = input("Year Applied (4 digits): ").strip()
                    date_applied = year_applied + "-" + month_applied + "-" + day_applied
                    result = input("Result: ").strip()
                    source = input("Source: ").strip()
                    link = input("Link: ").strip()
                    notes = input("Notes: ").strip()

                    add_application = ("INSERT INTO applications "
                                       "(company_name, position_name, date_applied, result, "
                                       "source, link, notes) "
                                       "VALUES (%s, %s, %s, %s, %s, %s, %s)")

                    application_data = (company_name, position_name, date_applied, result,
                                        source, link, notes)

                    cursor.execute(add_application, application_data)
                    cnx.commit()

                    print("Added")
                    print()
                elif user_input.lower().strip() == "e":
                    print()
                    break
                else:
                    print("Please enter one of the stated options.")
                    print()
        elif user_input.lower().strip() == "e":
            break
        else:
            print("Please enter one of the stated options.")
            print()

    print("Don't stop applying! You've got this! Make it a great day!")

    cursor.close()
    cnx.close()


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


if __name__ == "__main__":
    main()
