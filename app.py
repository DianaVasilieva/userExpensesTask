import database
from datetime import datetime
import matplotlib.pyplot as plt

MENU_PROMPT = """ ------ User`s expenses application ------ 

Please choose one of those option:

1) Add expenses in a category today or other particular day: (Ex: 2, food, 250, 04/12/2022);
2) Get whole statistic of expenses for a day, month or year;
3) Get statistic of expenses based on the category; 
4) Clear the data;
5) Add user;
6) Exit.

Your choice: """


def menu():
    connection = database.connect()
    database.create_table_user(connection)
    database.create_table_expenses(connection)

    try:
        while (user_input := int(input(MENU_PROMPT))) != 6:
            if user_input == 1:
                add_expenses_in_category(connection)
                file_output(connection)
            elif user_input == 2:
                date_statistic(connection)
            elif user_input == 3:
                category_statistic(connection)
            elif user_input == 4:
                clear_data(connection)
                file_output(connection)
            elif user_input == 5:
                add_users(connection)
                file_output(connection)
            elif user_input == 6:
                file_output(connection)
                quit()
    except ValueError:
        print("Invalid input, please try again!")
    except KeyboardInterrupt:
        print("Oops. Something went wrong.")


# FUNCTIONS FOR ALL THESE METHODS ABOVE
# TO WRITE DATA IN FILE
def file_output(connection):
    users = database.get_all_users(connection)
    expenses = database.get_all_expenses(connection)
    with open('users.txt', 'w') as f:
        f.write("user_id, first name, last name, phone \n")
        for line in users:
            f.write(str(line))
            f.write('\n')
    with open('expenses.txt', 'w') as f:
        f.write("expenses_id, user_id, category, value spent, day, month, year \n")
        for line in expenses:
            f.write(str(line))
            f.write('\n')

# 1
def add_expenses_in_category(connection):
    try:
        user_id = input("Enter user id (if you miss this field it will automatically add to 1 user): ")
        if len(user_id) == 0:
            user_id = 1
        category = input("Enter the category of expenses(food, clothes, etc): ")
        value = int(input(f"How much did you spend in hryvnias: "))
        count = input("Enter 1 - for today date and 2 - to input other date: ")
        if count == '1':
            data = datetime.now()
            day = data.strftime("%d")
            month = data.strftime("%m")
            year = data.strftime("%Y")
        else:

            date_time = input("Please input the date of expenses: (day/month/year): ")
            date_list = date_time.split("/")
            day = date_list[0]
            month = date_list[1]
            year = date_list[2]
        database.add_expenses(connection, user_id, category, value, day, month, year)
        print("The expense was added.")
    except ValueError:
        print("Invalid input, please try again!")
    except:
        print("Invalid input of data, please try again!")


# 4
def clear_data(connection):
    try:
        count = int(input("To clear the data from USERS - 1, from EXPENSES - 2, just clear WHOLE BOTH - 3: "))
        if count == 1:
            if len(database.get_all_users(connection)) == 0:
                print("The table is already empty.")
            else:
                choice = input("Do you want to delete USER - u ot TABLE OF USERS - tu: ")
                if choice == 'u':
                    user_id = input("Input user`s id who you want to delete: ")
                    database.delete_user_by_id(connection, user_id)
                    print("Cleared.")
                elif choice == 'tu':
                    database.delete_users(connection)
                    print("Cleared.")
        elif count == 2:
            if len(database.get_all_expenses(connection)) == 0:
                print("The table is already empty.")
            else:
                choice = input("Do you want to delete EXPENSES - e ot TABLE OF EXPENSES - te: ")
                if choice == 'e':
                    expenses_id = input("Input expenses id which you want to delete: ")
                    database.delete_expenses_by_id(connection, expenses_id)
                    print("Cleared.")
                elif choice == 'te':
                    database.delete_expenses(connection)
                    print("Cleared.")
        elif count == 3:
            if (len(database.get_all_users(connection)) and len(database.get_all_expenses(connection))) == 0:
                print("The tables are already empty.")
            else:
                database.delete_users(connection)
                database.delete_expenses(connection)
                print("Cleared.")
        else:
            print("We can not do anything with this input.")
    except ValueError:
        print("Invalid input, please try again!")


# 5
def add_users(connection):
    try:
        first_name = input("Enter user firstname: ")
        last_name = input("Enter user lastname: ")
        phone = input("Enter user phone: ")
        database.add_user(connection, first_name, last_name, phone)
    except BaseException:
        print("There is some error.")


# 2
def date_statistic(connection):
    try:
        now = datetime.now()
        question = input("If you want to see the user`s expenses statistic, write 'yes': ")
        if question == "yes":
            user_id = input("Please choose for which user do you want to see the statistic: ")
            choice = input("Please choose for which period you want to see statistic: day - d, month - m, year - y:")
            if choice == 'd':
                date_time = input("Please input the date of expenses: (day/month/year): ")
                date_list = date_time.split("/")
                day = date_list[0]
                month = date_list[1]
                year = date_list[2]
                one_user = database.get_one_user(connection, user_id)
                print("These expenses includes")
                whole_day = database.get_whole_expenses_user(connection, 1, day, month, year)
                print(f"The general amount of expenses used in {day}/{month}/{year} by {one_user[0]} {one_user[1]} "
                      f"is {whole_day[0]}")
                print("(category, expenses) - percent of the expenses from the entire price)")
                list_expenses = database.get_date_statistic_with_user_day(connection, user_id, day, month, year)
                list_for_data(list_expenses, whole_day)
            elif choice == 'm':
                date_time = input("Please input the month and year of expenses: (month/year): ")
                date_list = date_time.split("/")
                month = date_list[0]
                year = date_list[1]
                one_user = database.get_one_user(connection, user_id)
                print("These expenses includes")
                whole_month = database.get_whole_expenses_user(connection, 1, None, month, year)
                print(f"The general amount of expenses used in {month}/{year} by {one_user[0]} {one_user[1]} "
                      f"is {whole_month[0]}")
                print("(category, expenses) - percent of the expenses from the entire price)")
                list_expenses = database.get_date_statistic_with_user_month(connection, user_id, month, year)
                list_for_data(list_expenses, whole_month)
            elif choice == 'y':
                year = input("Please input the year of expenses: ")
                one_user = database.get_one_user(connection, user_id)
                print("These expenses for user includes")
                whole_year = database.get_whole_expenses_user(connection, 1, None, None, year)
                print(f"The general amount of expenses used in {year} by {one_user[0]} {one_user[1]}  "
                      f"is {whole_year[0]}")
                print("(category, expenses) - percent of the expenses from the entire price))")
                list_expenses = database.get_date_statistic_with_user_year(connection, user_id, year)
                list_for_data(list_expenses, whole_year)

        else:
            choice = input("Please choose for which period you want to see statistic: day - d, month - m, year - y:")
            if choice == 'd':
                date_time = input("Please input the date of expenses: (day/month/year): ")
                date_list = date_time.split("/")
                day = date_list[0]
                month = date_list[1]
                year = date_list[2]
                whole_day = database.get_whole_expenses(connection, day, month, year)
                print(f"The general amount of expenses used in {day}/{month}/{year} is {whole_day[0]}")
                print("(category, expenses) - percent of the expenses from the entire price))")
                list_expenses = database.get_date_statistic_day(connection, day, month, year)
                list_for_data(list_expenses, whole_day)
            elif choice == 'm':
                date_time = input("Please input the month and year of expenses: (month/year): ")
                date_list = date_time.split("/")
                month = date_list[0]
                year = date_list[1]
                whole_month = database.get_whole_expenses(connection, None, month, year)
                print(f"The general amount of expenses used in {month}/{year} is {whole_month[0]}")
                print("(category, expenses) - percent of the expenses from the entire price))")
                list_expenses = database.get_date_statistic_month(connection, month, year)
                list_for_data(list_expenses, whole_month)
            elif choice == 'y':
                year = input("Please input the year of expenses: ")
                whole_year = database.get_whole_expenses(connection, None, None, year)
                print(f"The general amount of expenses used in {year} is {whole_year[0]}")
                print("(category, expenses) - percent of the expenses from the entire price))")
                list_expenses = database.get_date_statistic_year(connection, year)
                list_for_data(list_expenses, whole_year)
    except ValueError:
        print("Incorrect value.")
    except SystemError:
        print("Oops. Something went wrong.")


# FUNCTION TO RETURN THE LISTS FOR STATISTIC(2)
def list_for_data(list_expenses, whole_period):
    new_list = []
    new_list_exp = []
    for i in list_expenses:
        x = int(i[1])
        res = (x * 100) / whole_period[0]
        new_list.append(round(res, 1))
    for i in list_expenses:
        new_list_exp.append(i)
    length = len(new_list_exp)
    for i in range(0, length):
        print(f"{new_list_exp[i]} - {new_list[i]} %")
    fig, ax = plt.subplots()
    my_dict = dict()

    # DIAGRAM OF EXPENSES
    for i in new_list_exp:
        if i[0] in my_dict:
            value = my_dict[i[0]]
            value += i[1]
            my_dict.update({i[0]: value})
        else:
            my_dict.update({i[0]: i[1]})

    ax.bar(my_dict.keys(), my_dict.values())
    ax.set_ylabel('Expenses values')
    ax.set_title('---Expenses by some period of time---')
    plt.show()


# 3
def category_statistic(connection):
    try:
        category = input("Please input category: ")
        if category == "all":
            list_expenses = database.get_all_category_statistic(connection)
            print(f"Category: {category}")
            for i in list_expenses:
                print(f"{i[0]} - {i[1]}")
        else:
            if len(database.get_category_statistic(connection, category)) != 0:
                question = input("If you want to see the user`s expenses statistic, write 'yes': ")
                if question == "yes":
                    user_id = input("Input the user id: ")
                    list_expenses = database.get_category_statistic_with_user(connection, user_id, category)
                    print(f"Category: {category}")
                    for i in list_expenses:
                        print(f"({i[0]}, {i[1]}/{i[2]}/{i[3]})")

                else:
                    list_expenses = database.get_category_statistic(connection, category)
                    print(f"Category: {category}")
                    for i in list_expenses:
                        print(f"({i[0]}, {i[1]}/{i[2]}/{i[3]})")
            else:
                print("There is no such category!")
    except BaseException:
        print("There is some error.")


menu()
