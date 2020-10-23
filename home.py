import pyrebase
from flask import Flask, render_template, request, flash,session,redirect,url_for,make_response
from firebase_admin import credentials, firestore, initialize_app
import re
import random, string
from forms import LoginForm,RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '1456780765656546'

firebaseConfig = {
    "apiKey": "AIzaSyBr5hMz8RQ7a8JsUVVwkjRJWGwczQe-uyM",
    "authDomain": "oceantest-121bd.firebaseapp.com",
    "databaseURL": "https://oceantest-121bd.firebaseio.com",
    "projectId": "oceantest-121bd",
    "storageBucket": "oceantest-121bd.appspot.com",
    "messagingSenderId": "654209058164",
    "appId": "1:654209058164:web:8318cfcc125b956fa49821",
    "measurementId": "G-NJZ9BP2M47"
  };


cred = credentials.Certificate("service.json")
default_app=initialize_app(cred)

db = firestore.client()
firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()

@app.route("/home",methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route("/",methods=['GET', 'POST'])
def general():
    return render_template('general.html')
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username=form.username.data
        email= form.email.data
        password=form.password.data
        reg=db.collection('register').document(email)
        doc={'username':username,'email':email,'passsword':password}
        auth.create_user_with_email_and_password(email, password)
        reg.set(doc)





        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        Email = form.email.data
        password = form.password.data
        try:
            if auth.sign_in_with_email_and_password(email, password):
                print("1")
                reg = db.collection('register').document(email).get().to_dict()
                print(reg)
                session['id'] = reg['username']


                flash('You have been logged in!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
                return render_template('login.html', title='Login', form=form)
        except:
            flash('Login Unsuccessful. Please check username and password', 'danger')
            return render_template('login.html', title='Login', form=form)
    return render_template('login.html', title='Login', form=form)
@app.route('/logout')
def logout():
    session.clear()
    return render_template('general.html')

@app.route("/profile")
def profile():
    return render_template('profile.html')


if __name__ == '__main__':
    app.run(debug=True)
