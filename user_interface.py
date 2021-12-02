class Ui:

    @staticmethod
    def run(cnx, cursor):
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

