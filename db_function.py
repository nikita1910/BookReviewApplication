import sqlite3
from sqlite3 import Error
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
database = os.path.join(THIS_FOLDER, 'BooksInfo.db')


def create_connection():
    """ create a database connection to the SQLite database
           specified by db_file
       :param db_file: database file
       :return: Connection object or None
       """
    conn = None
    try:
        conn = sqlite3.connect(database)
    except Error as e:
        print(f"Database connection error:\t{e}")
    return conn


def close_connection():
    """ close a database connection to the SQLite database
             :param conn:
             """
    try:
        conn = create_connection()
        conn.close()
    except Error as e:
        print(f"Database close connection error:\t{e}")


def get_user_password(param):
    """ Fetch password and username from DB
          :param:  userid
          :return: Password and user name
          """
    try:
        conn = create_connection()
        c = conn.cursor()
        data = c.execute("SELECT password,name FROM login where userid = ?", (param[0],))
        conn.commit()
        return data.fetchall()
    except Error as e:
        print(f"Select SQL execution error:\t{e}")


def get_All_login():
    """ Function call to reset password page in database
               :param: none
               :return: renders ResetPasswordPage page
              """
    try:
        conn = create_connection()
        c = conn.cursor()
        data = c.execute("select userid from login")
        conn.commit()
        return data
    except Error as e:
        print(f"Error occurred while executing get_All_login():\t{e}")


def save_user_details(user_data):
    """ Function call to save user details in database
              :param: uername, password and name
              :return: none
              """
    try:
        conn = create_connection()
        c = conn.cursor()
        # print(userdata)
        c.execute("INSERT INTO login(userid,password,name) VALUES(?,?,?)",
                  (user_data['username'][0], user_data['pwd'][0], user_data['name'][0]))
        conn.commit()
    except Error as e:
        print(f"Insert SQL execution error:\t{e}")


def get_book_data(param):
    """ Function call to get book isbn, title and  author from database
           :param: none
           :return: isbn, title and author
           """
    try:
        conn = create_connection()
        c = conn.cursor()
        # print(param)
        data = c.execute("select  isbn, title, author from books where isbn like ? or title = ? or author =?",
                         ('%' + param + '%', '%' + param + '%',
                          '%' + param + '%'))
        conn.commit()
        return data.fetchall()
    except Error as e:
        print(f"Insert SQL execution error:\t{e}")


def get_user_review(param):
    """ Function call fetch reviews from database
              :param: isbn
              :return: userid, username, userreview
              """
    try:
        conn = create_connection()
        c = conn.cursor()
        data = c.execute("select userid, username, userreview, rating from review where isbn =?",
                         (param,))
        conn.commit()
        return data.fetchall()
    except Error as e:
        print(f"User review select SQL execution error:\t{e}")


def save_rate_review(param, user_details_dict):
    """ Function call save rate and reviews in database
              :param: isbn, userid, name, rating,review
              :return: none
              """
    try:
        conn = create_connection()
        c = conn.cursor()
        # print(param)
        c.execute("INSERT INTO review(isbn,userid,username,userreview,rating) VALUES(?,?,?,?,?)",
                  (param['isbn'][0], user_details_dict['user_id'], user_details_dict['name'], param['review'][0],
                   param['rate'][0]))
        conn.commit()
    except Error as e:
        print(f" Error while inserting data in review table:\t{e}")


def update_user_password(param):
    """ Function call update password in database
             :param: user id
             :return: none
             """
    try:
        conn = create_connection()
        c = conn.cursor()
        c.execute("update login set password = ? where userid=?", (param['newpwd'][0], param['userid'][0]))
        conn.commit()
    except Error as e:
        print(f"Error occurred while updating password:\t{e}")
