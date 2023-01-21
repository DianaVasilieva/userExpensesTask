import sqlite3

CREATE_USER_TABLE = '''CREATE TABLE IF NOT EXISTS users(
user_id INTEGER PRIMARY KEY NOT NULL,
first_name TEXT NOT NULL,
last_name TEXT NOT NULL,
phone TEXT NOT NULL);'''
CREATE_EXPENSES_TABLE = """CREATE TABLE IF NOT EXISTS expenses(
expenses_id INTEGER PRIMARY KEY,
user_id INTEGER,
category TEXT,
value INTEGER,
day TEXT,
month TEXT,
year TEXT);"""

INSERT_USER = "INSERT INTO users (first_name, last_name, phone) VALUES (?, ?, ?);"
INSERT_EXPENSES = "INSERT INTO expenses(user_id, category, value, day, month, year) VALUES (?,?,?,?,?,?);"

GET_ALL_USERS = "SELECT * FROM users;"
GET_ALL_EXPENSES = "SELECT * FROM expenses;"
GET_USER = "SELECT first_name, last_name FROM users WHERE user_id = ?"

CHECK_FOR_SAME_USER = "SELECT * FROM users WHERE first_name = ? AND last_name = ? AND phone = ?;"
# DELETING ALL TABLE DATA
DELETE_DATA_USERS = "DELETE FROM users"
DELETE_DATA_EXPENSES = "DELETE FROM expenses"
# DELETE ROW
DELETE_ROW_USERS = "DELETE FROM users WHERE user_id = ?;"
DELETE_ROW_EXPENSES = "DELETE FROM expenses WHERE expenses_id = ?;"

# DELETE_ROW_EXPENSES_MAX = "DELETE FROM expenses WHERE ID=(SELECT MAX(expenses_id) FROM expenses);"
# MAX_EXPENSE_ID = "SELECT MAX(expenses_id) FROM expenses;"
# GET STATISTIC BY CATEGORIES
GET_STATISTIC_CATEGORY = "SELECT value, day, month,year FROM expenses WHERE category = ? ;"
GET_STATISTIC_CATEGORY_USER = "SELECT value, day, month,year FROM expenses WHERE user_id = ? AND category = ?;"
GET_STATISTIC_CATEGORY_ALL = "SELECT category, SUM(value) AS totL FROM expenses GROUP BY category; "

# VALUE OF WHOLE EXPENSES FOR STATISTIC WITH USER
GET_STATISTIC_YEAR_USER = "SELECT SUM(value)  FROM expenses  WHERE user_id = ? AND year = ?;"
GET_STATISTIC_MONTH_USER = "SELECT SUM(value) FROM expenses  WHERE user_id = ? " \
                           "AND month = ? AND year = ?;"
GET_STATISTIC_DAY_USER = "SELECT SUM(value) FROM expenses WHERE user_id = ? " \
                         "AND day = ? AND month = ? AND year = ? ;"

# VALUE OF WHOLE EXPENSES FOR STATISTIC WITHOUT USER
GET_STATISTIC_YEAR = "SELECT SUM(value)  FROM expenses  WHERE  year = ?;"
GET_STATISTIC_MONTH = "SELECT SUM(value) FROM expenses  WHERE month = ? AND year = ?;"
GET_STATISTIC_DAY = "SELECT SUM(value) FROM expenses WHERE day = ? AND month = ? AND year = ?;"

# STATISTIC DATE OF PARTICULAR USER
GET_STATISTIC_DATE_USER_DAY = "SELECT category, value FROM expenses WHERE user_id = ? " \
                              "AND day = ? AND month = ? AND year = ? ; "
GET_STATISTIC_DATE_USER_MONTH = "SELECT category, value FROM expenses WHERE user_id = ?  AND month = ? AND year = ?; "
GET_STATISTIC_DATE_USER_YEAR = "SELECT category, value FROM expenses WHERE user_id = ? AND year = ?; "

# STATISTIC DATE
GET_STATISTIC_DATE_DAY = "SELECT category, value FROM expenses WHERE day = ? AND month = ? " \
                         "AND year = ?; "
GET_STATISTIC_DATE_MONTH = "SELECT category, value FROM expenses WHERE  month = ? AND year = ?; "
GET_STATISTIC_DATE_YEAR = "SELECT category, value FROM expenses WHERE  year = ?;"


def connect():
    return sqlite3.connect('data.db')


# TABLES CREATION
def create_table_user(connection):
    with connection:
        connection.execute(CREATE_USER_TABLE)
        connection.commit()


def create_table_expenses(connection):
    with connection:
        connection.execute(CREATE_EXPENSES_TABLE)
        connection.commit()


# DATA ADDING
def add_user(connection, first_name, last_name, phone):
    if connection.execute(CHECK_FOR_SAME_USER, (first_name, last_name, phone)).fetchone():
        print("This user already exists!")
    else:
        connection.execute(INSERT_USER, (first_name, last_name, phone))
        connection.commit()
        print("The user was added.")


def add_expenses(connection, user_id, category, value, day, month, year):
    with connection:
        connection.execute(INSERT_EXPENSES, (user_id, category, value, day, month, year))


# DATA DELETING
def delete_users(connection):
    with connection:
        connection.execute(DELETE_DATA_USERS)
        connection.commit()


def delete_user_by_id(connection, user_id):
    with connection:
        connection.execute(DELETE_ROW_USERS, (user_id,))
        connection.commit()


def delete_expenses(connection):
    with connection:
        connection.execute(DELETE_DATA_EXPENSES)
        connection.commit()


def delete_expenses_by_id(connection, expenses_id):
    with connection:
        connection.execute(DELETE_ROW_EXPENSES, (expenses_id,))
        connection.commit()


# SELECT ALL
def get_all_users(connection):
    with connection:
        return connection.execute(GET_ALL_USERS).fetchall()


def get_all_expenses(connection):
    with connection:
        return connection.execute(GET_ALL_EXPENSES).fetchall()


# GET DATES STATISTICS OF ALL USERS
def get_date_statistic_day(connection, day, month, year):
    with connection:
        return connection.execute(GET_STATISTIC_DATE_DAY, (day, month, year)).fetchall()


def get_date_statistic_month(connection, month, year):
    with connection:
        return connection.execute(GET_STATISTIC_DATE_MONTH, (month, year)).fetchall()


def get_date_statistic_year(connection, year):
    with connection:
        return connection.execute(GET_STATISTIC_DATE_YEAR, [year]).fetchall()


# STATISTIC DATE OF PARTICULAR USER
def get_date_statistic_with_user_day(connection, user_id, day, month, year):
    with connection:
        res = connection.execute(GET_STATISTIC_DATE_USER_DAY, (user_id, day, month, year)).fetchall()
    return res


def get_date_statistic_with_user_month(connection, user_id, month, year):
    with connection:
        return connection.execute(GET_STATISTIC_DATE_USER_MONTH, (user_id, month, year)).fetchall()


def get_date_statistic_with_user_year(connection, user_id, year):
    with connection:
        return connection.execute(GET_STATISTIC_DATE_USER_YEAR, (user_id, year)).fetchall()


# GET STATISTIC BY CATEGORIES
def get_category_statistic(connection, category):
    with connection:
        return connection.execute(GET_STATISTIC_CATEGORY, [category]).fetchall()


def get_all_category_statistic(connection):
    with connection:
        return connection.execute(GET_STATISTIC_CATEGORY_ALL).fetchall()


def get_category_statistic_with_user(connection, user_id, category):
    with connection:
        return connection.execute(GET_STATISTIC_CATEGORY_USER, (user_id, category)).fetchall()


# WHOLE EXPENSES OF USER
def get_whole_expenses_user(connection, user_id, day, month, year):
    with connection:
        if day is not None:
            return connection.execute(GET_STATISTIC_DAY_USER, (user_id, day, month, year)).fetchone()
        elif month is not None:
            return connection.execute(GET_STATISTIC_MONTH_USER, (user_id, month, year)).fetchone()
        else:
            return connection.execute(GET_STATISTIC_YEAR_USER, (user_id, year)).fetchone()


# WHOLE EXPENSES
def get_whole_expenses(connection, day, month, year):
    with connection:
        if day is not None:
            return connection.execute(GET_STATISTIC_DAY, (day, month, year)).fetchone()
        elif month is not None:
            return connection.execute(GET_STATISTIC_MONTH, (month, year)).fetchone()
        else:
            return connection.execute(GET_STATISTIC_YEAR, [year]).fetchone()


# ONE USER OUTPUT
def get_one_user(connection, user_id):
    with connection:
        return connection.execute(GET_USER, [user_id]).fetchone()
