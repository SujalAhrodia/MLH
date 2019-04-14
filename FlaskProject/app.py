from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import json
from base64 import b64decode


app = Flask(__name__)
 
@app.route('/')
def home():
    if not session.get('logged_in'):
        session['image_iden'] = False
        return render_template('login.html')
    else:
        return "Welcome to the system!  <a href='/logout'>Logout</a>"
 
@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['first_name'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@app.route('/register', methods=['POST'])
def do_admin_register():
    if request.form['password'] != request.form['confirm_password']:
        flash('Wrong password!')
        return create_account()
    firstName = request.form['first_name']
    lastName = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    session['email'] = email
    new_object = {}
    new_object["firstName"] = firstName
    new_object["lastName"] = lastName
    new_object["password"] = password

    with open("data.json","r") as f:
        data = json.load(f)

    data[email] = new_object

    with open("data.json", "w") as jsonFile:
        json.dump(data, jsonFile)

    return image_recorder()


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route("/signup")
def signup():
    return render_template('signup.html')
 
@app.route("/data")
def data():
    return render_template('data.html')

@app.route("/file_save", methods=['POST'])
def do_file_save():
    data_uri = request.form['uri']
    print(session['email'])
    header, encoded = data_uri.split(",", 1)
    data = b64decode(encoded)

    with open("./static/people/image.jpg", "wb") as f:
        f.write(data)
    
    return render_template('/')


@app.route("/create_account")
def create_account():
    return render_template('create_account.html')

@app.route("/image_recorder", methods=['GET','POST'])
def image_recorder():
    return render_template('image_recorder.html')

@app.route("/login_email")
def login_email():
    return render_template('login_email.html')

@app.route("/login_email_register", methods=['POST'])
def do_email_login():
    return home()


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
