from flask import Flask, render_template, url_for, request, session, redirect
from pymongo import MongoClient
from flask_pymongo import PyMongo

app = Flask(__name__)

#app.config['MONGO_DBNAME'] = 'aavinash1083'
#app.config['MONGO_URI'] = "mongodb+srv://aavinash1083:9087828441@cluster0.9lbw1.mongodb.net/aavinash1083?retryWrites=true&w=majority"

#app.config['SECRET_KEY'] = 'aavvii'
#mongo = PyMongo(app)
cluster = MongoClient("mongodb+srv://crud:san@cluster0.mgpjl.mongodb.net/Contact_Info?retryWrites=true&w=majority")
db = cluster.Contact_Info
collections = db.Details
@app.route('/')
def index():
    if 'username' in session:
        return render_template('Dashboard.html',username = session['username'])

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    users = collections
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if (login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))
            return render_template('Dashboard.html')

    return 'Invalid username/password combination'
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = collections
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = (request.form['pass'])
            users.insert({'name' : request.form['username'], 'password' : hashpass, 'Email ID' : request.form['Email ID'], 'Phone Number' : request.form['Phone Number'] })
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html')

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
