from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import md5
import re

app = Flask(__name__)
app.secret_key = "ThisIsSecret!"

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile('^(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]')

mysql = MySQLConnector(app,'login_reg')

@app.route('/')
def index():
    # email = request.form['email']
    query = "SELECT * FROM users"
    # define your query
    users = mysql.query_db(query)
    # print "Hello"
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    error_count = 0;
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    pw_confirm = request.form['pw_confirm']
    hashed_password = md5.new(password).hexdigest()
    hashed_pw_confirm = md5.new(pw_confirm).hexdigest()
    print hashed_password
    if len(first_name) < 3:
        flash("First name must be longer than 2 characters!")
        error_count += 1
        print "Error Count: ", error_count, " - First Name Error"
    if len(last_name) < 3:
        flash("First name must be longer than 2 characters!")
        error_count += 1
        print "Error Count: ", error_count, " - Last Name Error"
    if not EMAIL_REGEX.match(email):
        flash("Invalid Email Address!")
        error_count += 1
        print "Error Count: ", error_count, " - Email Error"
    if len(password) < 8:
        flash("Password must be longer than 8 characters!")
        error_count += 1
        print "Error Count: ", error_count, " - Password Error"
    # if not PW_REGEX.match(pw_confirm):
    #     flash("Passwords must match")
    #     error_count += 1
    #     print "Error Count: ", error_count, " - Password Error"
    if password != pw_confirm:
        flash("passwords must match!")
    else:
        if error_count == 0:
            data = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'hashed_password': hashed_password,
                'pw_confirm': pw_confirm
            }
            query = "INSERT INTO users (first_name, last_name, email, password, pw_confirm, created_at, updated_at) VALUES (:first_name, :last_name, :email, :hashed_password, :pw_confirm, NOW(), NOW())"
            mysql.query_db(query, data)
            print "goes here"
            return redirect('/success')
            print users
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    data = {
        'email': request.form['email'],
        'password': request.form['password']
    }
    query1 = "SELECT * from users where email = :email"
    output1 = mysql.query_db(query1, data)
    query2 = "SELECT * from users where password = :password"
    output2 = mysql.query_db(query2, data)

    if len(output1) == 0:
        if len(output2) == 0:
            flash("Error! Type in the correct info to login!")
            return redirect('/')
        else:
            flash("Successfully logged in")
    return redirect('/success')

@app.route('/success')
def success():
    query = "SELECT * FROM users"
    # users = mysql.query_db(query)
    users = mysql.query_db(query)
    # return "goes here"
    return render_template('success.html', all_users=users)
    # , last_name, email, hashed_password)

app.run(debug=True)
