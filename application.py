import requests
from flask import Flask, render_template, request
import xmltodict
import re
import db_function
import sys

app = Flask(__name__, template_folder='templates')

user_details_dict = {"user_id": '', "name": ''}


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

            if db_function.create_connection() is not None:
                user_details = db_function.get_user_password(credentials['email'])
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
    except Exception:
        print(f"Error occurred while executing LoginPage():\t", sys.exc_info()[0])


@app.route('/new_acc', methods=["GET"])
def new_acc():
    """ Function call to create new account page
             :param: none
             :return: renders CreateAccountPage page
            """
    lst_login = []
    try:
        if db_function.create_connection() is not None:
            login = db_function.get_All_login()
            for x in login.fetchall():
                lst_login.append(x[0])
            return render_template("CreateAccountPage.html", user_ids=lst_login)
        else:
            print("Error! cannot create the database connection.")
    except Exception:
        print(f"Error occurred while executing new_acc():\t", sys.exc_info()[0])


@app.route('/save_new_user_details', methods=["POST"])
def save_new_user_details():
    """ Function to call DB function to save new user details page
                :param: none
                :return: renders CreateAccountPage page
               """
    try:
        if request.method == "POST":
            new_user_details = request.form.to_dict(flat=False)

            if db_function.create_connection() is not None:
                db_function.save_user_details(new_user_details)
            else:
                print("Error! cannot create the database connection.")
            return render_template("LoginPage.html")
    except Exception:
        print(f"Error occurred while executing save_new_user_details():\t", sys.exc_info()[0])


@app.route('/search_page', methods=["GET"])
def search_page():
    """ Function call to search books
       :param: none
       :return: renders SearchPage page
       """
    try:
        return render_template("SearchPage.html", userid=user_details_dict['user_id'], name=user_details_dict['name'],
                               book_info='')
    except Exception:
        print(f"Error occurred while executing search_page():\t", sys.exc_info()[0])


@app.route('/reset_pwd', methods=["GET"])
def reset_pwd():
    """ Function call to reset password page
             :param: none
             :return: renders ResetPasswordPage page
            """
    lst_login = []
    try:
        if db_function.create_connection() is not None:
            login = db_function.get_All_login()
            for x in login.fetchall():
                lst_login.append(x[0])
        else:
            print("Error! cannot create the database connection.")
        return render_template("ResetPasswordPage.html", logins=lst_login)
    except Exception:
        print(f"Error occurred while executing reset_pwd():\t", sys.exc_info()[0])


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
            if db_function.create_connection() is not None:
                book_info = db_function.get_book_data(data['searchElement'][0])
                # print(list(book_info.fetchall()))
                return render_template("SearchPage.html", userid=user_details_dict['user_id'], book_info=book_info,
                                       name=user_details_dict['name'])
            else:
                print("Error! cannot create the database connection.")

    except Exception:
        print(f"Error occurred while executing get_book_info():\t", sys.exc_info()[0])


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
    except Exception:
        print(f"Error occurred while executing get_API_book_info():\t", sys.exc_info()[0])


@app.route('/check_review', methods=["POST"])
def check_review():
    """ Function call check book reviews
           :param: none
           :return: renders ReviewPage page
           """
    try:
        data = request.form
        data = data.to_dict(flat=False)
        bookDetails = get_API_book_info(data['isbn'][0])
        regex = re.compile(r'<[^>]+>')

        return render_template("ReviewPage.html", bookDetails=bookDetails,
                               description=regex.sub('', bookDetails['description']),
                               userreview=db_function.get_user_review(data['isbn'][0]), name=user_details_dict['name'])
    except Exception:
        print(f"Error occurred while executing check_review():\t", sys.exc_info()[0])


@app.route('/submit_review_rating', methods=["POST"])
def submit_review_rating():
    """ Function call to submit user book reviews
             :param: none
             :return: renders ReviewPage page with user reviews
             """
    try:
        data = request.form
        data = data.to_dict(flat=False)
        if db_function.create_connection() is not None:
            db_function.save_rate_review(data, user_details_dict)
        else:
            print("Error! cannot create the database connection.")

        bookDetails = get_API_book_info(data['isbn'][0])
        regex = re.compile(r'<[^>]+>')

        return render_template("ReviewPage.html", bookDetails=bookDetails,
                               description=regex.sub('', bookDetails['description']),
                               userreview=db_function.get_user_review(data['isbn'][0]), name=user_details_dict['name'])
    except Exception:
        print(f"Error occurred while executing submit_review_rating():\t", sys.exc_info()[0])


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
            if db_function.create_connection() is not None:
                db_function.update_user_password(data)
            else:
                print("Error! cannot create the database connection.")
        db_function.close_connection()
        return render_template("LoginPage.html")
    except Exception:
        print(f"Error occurred while executing main_login():\t", sys.exc_info()[0])


@app.route('/app_info', methods=['GET'])
def app_info():
    """ Function call to get information about application
             :param: none
             :return: renders AboutUsPage page
             """
    try:
        return render_template("AboutUsPage.html")
    except Exception:
        print(f"Error occurred while executing app_info():\t", sys.exc_info()[0])


@app.route('/app_service', methods=['GET'])
def app_service():
    """ Function call to know about application services
             :param: none
             :return: renders Services page
             """
    try:
        return render_template("Services.html")
    except Exception:
        print(f"Error occurred while executing app_service():\t", sys.exc_info()[0])


def main():
    pass


if __name__ == '__main__':
    main()
    app.run()
    # app.debug = True
