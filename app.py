from flask import Flask, render_template, request, session, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug import secure_filename
from flask_mail import Mail
import json
import os
import math
from datetime import datetime


with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True
app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config['UPLOAD_FOLDER'] = params['upload_location']
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD = params['gmail-password'],
)
mail = Mail(app)
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)


class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)

    


@app.route("/")
def home():
    return render_template('index.html', params=params)


@app.route("/about")
def about():
    return render_template('about.html', params=params)

@app.route("/books")
def books():
    my_books = [{"id":1, "name": "Keep Moving", "picture" : "ik.jpg", "price1": "123.00","status":"lalala"},{"id":2,"name": "book 2", "picture" : "12.jpg", "price1": "124.00"}]
    return render_template('books.html', params=params, books = my_books)

@app.route("/cart")
def cart():
    return render_template('cart.html', params=params)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if ('user' in session and session ['user'] == params['admin_user']):
        posts = Posts.query.all()
        return render_template('welcome.html', params=params, posts=posts)

    if request.method=='POST':
        username=request.form.get('uname')
        userpass=request.form.get('pass')
        if (username == params['admin_user'] and userpass == params['admin_password']):
            #set the session variable
            session['user'] = username
            posts = Posts.query.all()
            return render_template('welcome.html', params=params, posts=posts)

    return render_template('login.html', params=params)





#@app.route("/logout")
#def logout():
#    session.pop('user')
#    return redirect('/login')



@app.route("/contact", methods = ['GET','POST'])
def contact():
    if(request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name=name, phone_num = phone, msg = message, date= datetime.now(),email = email, )
        db.session.add(entry)
        db.session.commit()
        #mail.send_message('New message from ' + name,
        #                 sender=email,
        #                recipients = [params['gmail-user']],
        #               body = message + "\n" + phone
        #              )
        
        flash("Thanks for submitting your details. We will get back to you soon", "success")
    return render_template('contact.html', params=params)


app.run(debug=True)
