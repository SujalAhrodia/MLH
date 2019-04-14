from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, Response, copy_current_request_context, redirect, url_for
from authenticate import VideoCamera
import os
import json
import random
from base64 import b64decode


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

@app.route('/')
def home():
    if not session.get('logged_in'):        
        return render_template('login.html')
    else:
        return "Welcome to the system!  <a href='/logout'>Logout</a>"



def generate_frame(camera):
    name_val = [] 
    flag = True   
    with app.test_request_context():
        while flag:
            frame, name = camera.run_face_recognition()
            name_val.append(name)
            if len(name_val)>=3 and name != None:
                if name_val[-3] == name_val[-2] and name_val[-2] == name_val[-1]:
                    # session['name'] = name_val[-3]
                    # session['image_iden'] = True
                    # print(name_val)
                    session['name'] = name
                    session['image_iden'] = True
                    # flag=False
                    # return redirect(url_for('home'))
                    # print(session['name'])
                    # break  
            
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
@app.route('/video')
def video_feed():
    return Response(generate_frame(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

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
    #session['email'] = email.split('@')[0]
    new_object = {}
    new_object["firstName"] = firstName
    new_object["lastName"] = lastName
    new_object["email"] = email
    #new_object["emailName"] = email.split('@')[0]
    new_object["password"] = password

    with open("data.json","r") as f:
        data = json.load(f)
        
    userName = firstName + lastName + str(random.randint(1,100))

    session["userName"] = userName
    data[userName] = new_object

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
 

@app.route("/login2")
def login2():
    return render_template('login2.html')

@app.route("/file_save", methods=['POST'])
def do_file_save():
    data_uri = request.form['uri']
    #print(session['email'])
    header, encoded = data_uri.split(",", 1)
    data = b64decode(encoded)
    path = "./static/people/"+session["userName"]+".jpg"
    with open(path, "wb") as f:
        f.write(data)
    return home()

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
    with open("data.json","r") as f:
        data = json.load(f)

    uEmail = request.form['email']

    if uEmail not in data.keys():
        flash("User doesn't exists.")
        return home()

    if request.form['password'] == data[uEmail]["password"]:
        session['logged_in'] = True
        session['email'] = True
    else:
        flash('Wrong password!')
        return home()
    return home()

if __name__ == "__main__":
    #socketio.run(app)
    app.run(debug= True, host='0.0.0.0', port=4000)
