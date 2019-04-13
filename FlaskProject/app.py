from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os

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
    return image_recorder()


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route("/signup")
def signup():
    return render_template('signup.html')
 
@app.route("/create_account")
def create_account():
    return render_template('create_account.html')

@app.route("/image_recorder", methods=['POST'])
def image_recorder():
    return render_template('image_recorder.html')

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
