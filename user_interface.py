import mysql


def print_column_names(cursor):
    print()

    column_info_tuple = cursor.description
    columns = ""

    for (column) in column_info_tuple:
        columns += str(column[0]) + ", "

    print(columns[:-2])


def print_rows(cursor):
    for (row) in cursor:
        row_as_string = ""
        for item in row:
            row_as_string += str(item) + ", "
        print(row_as_string[:-2])

    print()


def print_query_to_console(cursor):
    print_column_names(cursor)
    print_rows(cursor)


def execute_sql_query(cursor, query):
    try:
        cursor.execute(query)
        print_query_to_console(cursor)
    except mysql.connector.Error:
        print("Please enter a valid SQL Query.")
        print()


def run_sql_side(cursor):
    print("Welcome to the SQL side!")

    while True:
        query = input("Please enter a SQL query "
                      "(\"E\" to exit to the main menu): ")

        if query.lower().strip() == "e":
            print()
            break
        else:
            execute_sql_query(cursor, query)


def print_sans_sql_side_menu():
    print("Please choose on of the following options by entering its number:")
    print("1: View all applications")
    print("2: Add an application")
    print("3: Delete an application")
    print("(\"E\" to exit to the main menu)")
    user_input = input("")

    return user_input


def execute_sans_sql_query_view_all_applications(cursor):
    query = "SELECT * FROM applications"

    cursor.execute(query)
    print_query_to_console(cursor)


def get_application_data():
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
    print()

    return company_name, position_name, date_applied, result, source, link, notes


def execute_sans_sql_query_add_application(cursor, cnx):
    add_application = ("INSERT INTO applications "
                       "(company_name, position_name, date_applied, result, "
                       "source, link, notes) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s)")

    application_data = get_application_data()

    cursor.execute(add_application, application_data)
    cnx.commit()


def get_app_number_to_delete(cursor):
    execute_sans_sql_query_view_all_applications(cursor)
    app_no_to_delete = input("What is the app_no of the application "
                             "that you would like to delete? ")
    print()

    return app_no_to_delete


def execute_sans_sql_query_delete_application(cursor, cnx):
    app_no_to_delete = get_app_number_to_delete(cursor)

    delete_application = "DELETE FROM applications WHERE app_no =" + app_no_to_delete + ";"

    cursor.execute(delete_application)
    cnx.commit()


def run_sans_sql_side(cursor, cnx):
    print("Welcome to the sans-SQL side!")

    while True:
        user_input = print_sans_sql_side_menu()

        if user_input.strip() == "1":
            execute_sans_sql_query_view_all_applications(cursor)
        elif user_input.strip() == "2":
            execute_sans_sql_query_add_application(cursor, cnx)
        elif user_input.strip() == "3":
            execute_sans_sql_query_delete_application(cursor, cnx)
        elif user_input.lower().strip() == "e":
            print()
            break
        else:
            print("Please enter one of the stated options.")
            print()


class Ui:

    @staticmethod
    def run(cnx, cursor):
        print("Welcome to the Application Tracker!")

        while True:
            print("Would you like to use SQL to work with your application data or not?")
            user_input = input("Please enter \"S\" for SQL or \"N\" for without SQL "
                               "(\"E\" to exit): ")
            print()

            if user_input.lower().strip() == "s":
                run_sql_side(cursor)
            elif user_input.lower().strip() == "n":
                run_sans_sql_side(cursor, cnx)
            elif user_input.lower().strip() == "e":
                break
            else:
                print("Please enter one of the stated options.")
                print()

        print("\033[92m" + "Don't stop applying! You've got this! Make it a great day!")

        cursor.close()
        cnx.close()
