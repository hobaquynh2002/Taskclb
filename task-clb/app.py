# from flask import Flask, url_for, render_template, request, redirect, session
# import flask
# from flask import request, jsonify
# from flask_cors import CORS
# import mysql.connector
# from werkzeug.utils import secure_filename
# import os
# # App Config
# app = flask.Flask(__name__)
# CORS(app)
# app.config['UPLOAD_FOLDER']='/home/kali/Desktop/task-clb/static/'
# app.config["SESSION_TYPE"] = "filesystem"
# ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])
# # Database Config
# db_config = {
# "user": "root",
# "password": "123456a@",
# "database": "users_db"
# }
# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
# @app.route('/', methods=['GET'])
# def index():
#     if session.get('logged_in'):
#         return render_template('profile.html',msg=u'\U0001f604')
#     else:
#         return render_template('index.html',msg='Welcome to the page!')

# @app.route('/register/', methods=['GET', 'POST'])
# def register():
#     msg = ''
#     if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
#         try:# Create variables for easy access
#             username = request.form['username']
#             password = request.form['password']
#             email = request.form['email']
#             # Connect to database
#             conn = mysql.connector.Connect(**db_config)
#             cursor = conn.cursor()
#             query = "SELECT * FROM users WHERE username = %s OR email = %s"
#             cursor.execute(query, (username, email))

#             if cursor.fetchone():
#                 msg = 'Error! This username or email already exists.'
#                 return render_template('register.html', msg=msg)
#             else:
#                 # Create entry in DB
#                 query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
#                 cursor.execute(query, (username, password, email))
#                 conn.commit() 
#                 return redirect(url_for('login'))
#         except:
#             return render_template('index.html',msg=u'\U0001f604')      
#     else:
#         msg = 'Error!'
#         return render_template('register.html', msg=msg)

# @app.route('/login/', methods=['GET', 'POST'])
# def login():
#     msg = ''
#     if request.method == 'GET':
#         return render_template('index.html',msg='Hello!')
#     else:
#     # Read data from request
#         username  = request.form['username']
#         password  = request.form['password']

#         # Connect to database
#         conn = mysql.connector.Connect(**db_config) 
#         cursor = conn.cursor()

#         # Find user in DB
#         query = "SELECT * FROM users WHERE username = %s AND password = %s"
#         cursor.execute(query, (username, password))
#         users = cursor.fetchall()
#         # Return success or failure
#         if users:
#             session['loggedin'] = True
#             # Redirect to profile
#             return redirect(url_for('profile',username=username))
#         else:
#             msg = 'Incorrect username/password!'
#             return render_template('login.html',msg=msg)

# @app.route('/profile/<username>',methods=['GET','POST'])
# def profile(username):
#     user=username
#     filename = None
#     if request.method == 'POST' and session['loggedin']:
#         file= request.files['file']
#         filename = secure_filename(file.filename)
#         filename='admin'+'.png'
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         return redirect(url_for('display_file',filename=filename))
#     elif request.method == 'GET' and session['loggedin']:
#         filename=user+'.png'
#         return render_template('profile.html',uploaded_file=url_for('static',filename=filename),username=user)
#     elif not session['loggedin']:
#         return redirect(url_for('logout'))

# @app.route('/uploads/<filename>')
# def display_file(filename):
#     if session['loggedin']:
#         return render_template('profile.html',uploaded_file=url_for('static',filename=filename))
#     if not session['loggedin']:   
#         return redirect(url_for('logout'))
# @app.route('/logout', methods=['GET'])
# def logout():
#     session.pop('loggedin', None)
#     return redirect(url_for('login'))

# if __name__ == "__main__":
#     app.secret_key = "ThisIsNotASecret:p"
#     app.run(debug=True)
