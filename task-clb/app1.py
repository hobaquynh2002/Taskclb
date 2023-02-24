from flask import Flask, url_for, render_template, request, redirect, session
import flask
from flask import request, jsonify
from flask_cors import CORS
import mysql.connector
from werkzeug.utils import secure_filename
import os
import hashlib
# App Config
app = flask.Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER']='/home/kali/Desktop/task-clb/static/'
app.config["SESSION_TYPE"] = "filesystem"
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])
# Database Config
db_config = {
"user": "root",
"password": "123456a@",
"database": "users_db"
}

@app.route('/', methods=['GET'])
def index():
    if session.get('logged_in'):
        return render_template('profile.html',msg=u'\U0001f604')
    else:
        return render_template('index.html',msg='Welcome to the page!')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        try:# Create variables for easy access
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            # Connect to database
            conn = mysql.connector.Connect(**db_config)
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE username = %s OR email = %s"
            cursor.execute(query, (username, email))

            if cursor.fetchone():
                msg = 'Error! This username or email already exists.'
                return render_template('register.html', msg=msg)
            else:
                # Create entry in DB
                query = "INSERT INTO users (username, password, email,filename) VALUES (%s, %s, %s,%s)"
                cursor.execute(query, (username, password, email,''))
                conn.commit() 
                return redirect(url_for('login'))
        except:
            return render_template('index.html',msg=u'\U0001f604')      
    else:
        msg = '<3'
        return render_template('register.html', msg=msg)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'GET':
        return render_template('index.html',msg='Hello!')
    else:
    # Read data from request
        username  = request.form['username']
        password  = request.form['password']

        # Connect to database
        conn = mysql.connector.Connect(**db_config) 
        cursor = conn.cursor()

        # Find user in DB
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        users = cursor.fetchall()
        # Return success or failure
        if users:
            session['loggedin'] = True
            session['user_login'] = username
            # Redirect to profile
            return redirect(url_for('profile',username=session['user_login']))
        else:
            msg = 'Incorrect username/password!'
            return render_template('index.html',msg=msg)

@app.route('/profile/<username>',methods=['GET','POST'])
def profile(username):
    if session['user_login']!=username:
        return redirect(url_for('forbidden'))
    filename = None
    conn = mysql.connector.Connect(**db_config)
    cursor = conn.cursor()
    if request.method == 'POST' and session['loggedin']:
        file= request.files['file']
        filename = secure_filename(file.filename)
        query ="UPDATE users SET filename=%s WHERE username = %s"
        cursor.execute(query, (filename,session['user_login']))
        conn.commit() 
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('display_file',filename=filename))
    elif request.method == 'GET' and session['loggedin']:
        query = "SELECT filename FROM users WHERE username = %s"
        cursor.execute(query, (session['user_login'],))
        return render_template('profile.html', uploaded_file=url_for('static', filename=cursor.fetchone()[0]), username=session['user_login'])
    elif not session['loggedin']:
        return redirect(url_for('logout'))

@app.route('/uploads/<filename>')
def display_file(filename):
    if session['loggedin']:
        return render_template('profile.html',uploaded_file=url_for('static',filename=filename))
    if not session['loggedin']:   
        return redirect(url_for('logout'))
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('loggedin', None)
    session.pop('user_login', None)
    return redirect(url_for('login'))
@app.route('/forbidden')
def forbidden():
    session.pop('loggedin', None)
    session.pop('user_login', None)
    return render_template('forbidden.html')


if __name__ == "__main__":
    app.secret_key = "ThisIsNotASecret:p"
    app.run(debug=True)
