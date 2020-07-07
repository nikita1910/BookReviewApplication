import requests
import sqlite3
from sqlite3 import Error
from flask import Flask, render_template, request
import os
import xmltodict
import re

app = Flask(__name__, template_folder='templates')

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
database = os.path.join(THIS_FOLDER, 'BooksInfo.db')
user_details_dict = {"user_id": '', "name": ''}


def create_connection(db_file):
    """ create a database connection to the SQLite database
           specified by db_file
       :param db_file: database file
       :return: Connection object or None
       """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(f"Database connection error:\t{e}")
    return conn


def main():
    pass


def close_connection(conn):
    """ close a database connection to the SQLite database
             :param conn:
             """
    try:
        conn.close()
    except Error as e:
        print(f"Database close connection error:\t{e}")


def get_user_password(conn, user_id):
    """ Fetch password and username from DB
          :param user_id:
          :param conn:
          :return: Password and user name
          """
    data = ''
    try:
        c = conn.cursor()
        data = c.execute("SELECT password,name FROM login where userid = ?", (user_id[0],))

    except Error as e:
        print(f"Select SQL execution error:\t{e}")
    conn.commit()
    return data.fetchall()


@app.route('/', methods=["GET", "POST"])
def LoginPage():
    """ Function call to load login page
           :param: none
           """
    global user_details_dict
    try:
        if request.method == "POST":
            credentials = request.form
            credentials = credentials.to_dict(flat=False)
            conn = create_connection(database)
            if conn is not None:
                user_details = get_user_password(conn, credentials['email'])
                close_connection(conn)
                # print(pwd)
                if not len(user_details) == 0:
                    # print(credentials['password'][0])
                    if user_details[0][0] == credentials['password'][0]:
                        user_details_dict['user_id'] = credentials['email'][0]
                        user_details_dict['name'] = user_details[0][1]
                        return render_template("SearchPage.html", userid=user_details_dict['user_id'],
                                               name=user_details_dict['name'], book_info='')
                    else:
                        return render_template("LoginPage.html",
                                               errorMsg="Incorrect username or password.")
                else:
                    return render_template("LoginPage.html", errorMsg="Email or password is incorrect. Try again or "
                                                                      "click Forgot password to reset it.")
            else:
                print("Error! cannot create the database connection.")
        else:
            return render_template("LoginPage.html")
    except Error as e:
        print(f"Error occurred while executing LoginPage():\t{e}")


@app.route('/new_acc', methods=["GET"])
def new_acc():
    """ Function call to create new account page
             :param: none
             :return: renders CreateAccountPage page
            """
    lst_login = []
    try:
        conn = create_connection(database)
        if conn is not None:
            login = get_All_login(conn)
            for x in login.fetchall():
                lst_login.append(x[0])
            close_connection(conn)
            return render_template("CreateAccountPage.html", user_ids=lst_login)
        else:
            print("Error! cannot create the database connection.")
    except Error as e:
        print(f"Error occurred while executing new_acc():\t{e}")


@app.route('/save_new_user_details', methods=["POST"])
def save_new_user_details():
    """ Function to call DB function to save new user details page
                :param: none
                :return: renders CreateAccountPage page
               """
    try:
        if request.method == "POST":
            new_user_details = request.form.to_dict(flat=False)
            conn = create_connection(database)
            if conn is not None:
                save_user_details(conn, new_user_details)
            else:
                print("Error! cannot create the database connection.")
            return render_template("LoginPage.html")
    except Error as e:
        print(f"Error occurred while executing save_new_user_details():\t{e}")


@app.route('/search_page', methods=["GET"])
def search_page():
    """ Function call to search books
       :param: none
       :return: renders SearchPage page
       """
    try:
        return render_template("SearchPage.html", userid=user_details_dict['user_id'], name=user_details_dict['name'],
                               book_info='')
    except Error as e:
        print(f"Error occurred while executing search_page():\t{e}")


def get_All_login(conn):
    """ Function call to reset password page in database
               :param: none
               :return: renders ResetPasswordPage page
              """
    try:
        c = conn.cursor()
        data = c.execute("select userid from login")
        conn.commit()
        return data
    except Error as e:
        print(f"Error occurred while executing get_All_login():\t{e}")


@app.route('/reset_pwd', methods=["GET"])
def reset_pwd():
    """ Function call to reset password page
             :param: none
             :return: renders ResetPasswordPage page
            """
    lst_login = []
    try:
        conn = create_connection(database)
        if conn is not None:
            login = get_All_login(conn)
            for x in login.fetchall():
                lst_login.append(x[0])
            close_connection(conn)
        else:
            print("Error! cannot create the database connection.")
        return render_template("ResetPasswordPage.html", logins=lst_login)
    except Error as e:
        print(f"Error occurred while executing reset_pwd():\t{e}")


def save_user_details(conn, user_data):
    """ Function call to save user details in database
              :param: uername, password and name
              :return: none
              """
    try:
        c = conn.cursor()
        # print(userdata)
        c.execute("INSERT INTO login(userid,password,name) VALUES(?,?,?)",
                  (user_data['username'][0], user_data['pwd'][0], user_data['name'][0]))
    except Error as e:
        print(f"Insert SQL execution error:\t{e}")
    conn.commit()
    close_connection(conn)


def get_book_data(conn, param):
    """ Function call to get book isbn, title and  author from database
           :param: none
           :return: isbn, title and author
           """
    data = ''
    try:
        c = conn.cursor()
        # print(param)
        data = c.execute("select  isbn, title, author from books where isbn like ? or title = ? or author =?",
                         ('%' + param + '%', '%' + param + '%',
                          '%' + param + '%'))
        conn.commit()
    except Error as e:
        print(f"Insert SQL execution error:\t{e}")

    return data.fetchall()


@app.route('/get_book_info', methods=["POST"])
def get_book_info():
    """ Function call to search books with book id
           :param: none
           :return: renders SearchPage page with all book details
           """
    try:
        if request.method == "POST":
            data = request.form
            data = data.to_dict(flat=False)
            conn = create_connection(database)
            if conn is not None:
                book_info = get_book_data(conn, data['searchElement'][0])
                # print(list(book_info.fetchall()))
                close_connection(conn)
                return render_template("SearchPage.html", userid=user_details_dict['user_id'], book_info=book_info,
                                       name=user_details_dict['name'])
            else:
                print("Error! cannot create the database connection.")

    except Error as e:
        print(f"Error occurred while executing get_book_info():\t{e}")


def get_API_book_info(isbn):
    """ Function call fetch book details via API
              :param: isbn
              :return: book details in XML format
              """
    try:
        res = requests.get("https://www.goodreads.com/book/isbn/" + isbn + "?key=RVrNHy0sfepuCVMw1ghmA")
        if res.status_code != 200:
            raise Exception("Error:API request unsuccessful.")
        return xmltodict.parse(res.content)['GoodreadsResponse']['book']
    except Error as e:
        print(f"Error occurred while executing get_API_book_info():\t{e}")


def get_user_review(conn, param):
    """ Function call fetch reviews from database
              :param: isbn
              :return: userid, username, userreview
              """
    data = ''
    try:
        c = conn.cursor()
        data = c.execute("select userid, username, userreview, rating from review where isbn =?",
                         (param,))
        conn.commit()
    except Error as e:
        print(f"User review select SQL execution error:\t{e}")
    return data.fetchall()


@app.route('/check_review', methods=["POST"])
def check_review():
    """ Function call check book reviews
           :param: none
           :return: renders ReviewPage page
           """
    try:
        data = request.form
        data = data.to_dict(flat=False)
        conn = create_connection(database)
        bookDetails = get_API_book_info(data['isbn'][0])
        regex = re.compile(r'<[^>]+>')

        return render_template("ReviewPage.html", bookDetails=bookDetails,
                               description=regex.sub('', bookDetails['description']),
                               userreview=get_user_review(conn, data['isbn'][0]), name=user_details_dict['name'])
    except Error as e:
        print(f"Error occurred while executing check_review():\t{e}")


def save_rate_review(conn, data):
    """ Function call save rate and reviews in database
              :param: isbn, userid, name, rating,review
              :return: none
              """
    try:
        c = conn.cursor()
        print(data)
        c.execute("INSERT INTO review(isbn,userid,username,userreview,rating) VALUES(?,?,?,?,?)",
                  (data['isbn'][0], user_details_dict['user_id'], user_details_dict['name'], data['review'][0],
                   data['rate'][0]))
    except Error as e:
        print(f" Error while inserting data in review table:\t{e}")
    conn.commit()


@app.route('/submit_review_rating', methods=["POST"])
def submit_review_rating():
    """ Function call to submit user book reviews
             :param: none
             :return: renders ReviewPage page with user reviews
             """
    try:
        data = request.form
        data = data.to_dict(flat=False)
        conn = create_connection(database)
        if conn is not None:
            save_rate_review(conn, data)
        else:
            print("Error! cannot create the database connection.")

        bookDetails = get_API_book_info(data['isbn'][0])
        regex = re.compile(r'<[^>]+>')

        return render_template("ReviewPage.html", bookDetails=bookDetails,
                               description=regex.sub('', bookDetails['description']),
                               userreview=get_user_review(conn, data['isbn'][0]), name=user_details_dict['name'])
    except Error as e:
        print(f"Error occurred while executing submit_review_rating():\t{e}")


def update_user_password(conn, data):
    """ Function call update password in database
             :param: user id
             :return: none
             """
    try:
        conn.cursor()
        conn.execute("update login set password = ? where userid=?", (data['newpwd'][0], data['userid'][0]))
    except Error as e:
        print(f"Error occurred while updating password:\t{e}")
    conn.commit()
    close_connection(conn)


@app.route('/main_login', methods=["GET", "POST"])
def main_login():
    """ Function call to load login page
             :param: none
             :return: renders LoginPage page
             """
    try:
        user_details_dict.update({}.fromkeys(user_details_dict, ''))
        # print(user_details_dict)
        if request.method == "POST":
            data = request.form
            data = data.to_dict(flat=False)
            conn = create_connection(database)
            if conn is not None:
                update_user_password(conn, data)
            else:
                print("Error! cannot create the database connection.")

        return render_template("LoginPage.html")
    except Error as e:
        print(f"Error occurred while executing main_login():\t{e}")


@app.route('/app_info', methods=['GET'])
def app_info():
    """ Function call to get information about application
             :param: none
             :return: renders AboutUsPage page
             """
    try:
        return render_template("AboutUsPage.html")
    except Error as e:
        print(f"Error occurred while executing app_info():\t{e}")


@app.route('/app_service', methods=['GET'])
def app_service():
    """ Function call to know about application services
             :param: none
             :return: renders Services page
             """
    try:
        return render_template("Services.html")
    except Error as e:
        print(f"Error occurred while executing app_service():\t{e}")


if __name__ == '__main__':
    main()
    app.run()
    # app.debug = True
