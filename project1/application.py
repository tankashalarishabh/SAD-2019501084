import csv
import sys
import os
from flask import Flask, session,request,render_template,flash,logging,redirect,url_for
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
from models import User,db
import time
from booksread import *
from imports import *
from userReview import *
from test import bookreview
from sqlalchemy import create_engine,desc
import json
from sqlalchemy import or_
import requests


app = Flask(__name__)

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key="email"

db.init_app(app)
def main():
    db.create_all()

# Check for environment variable


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))



@app.route("/")
def index():
    return "hello"

@app.route("/register", methods=["GET", "POST"])
def register():

    if (request.method == "POST"):
        mail = request.form['name']
        passw = request.form['pwd']

        # count = User.query.filter_by(email=mail).count()
        # print (count)
        try:
            register = User(email = mail, password = passw)
            db.session.add(register)
            db.session.commit()
            a=User.query.all()
            print(a)
            return render_template("register.html",name=mail)
        except:
            error="You have already registered with this email"
            return render_template("register.html",message=error)
    return render_template("register.html")

# @app.route("/login",methods=["GET","POST"])
# def login():
#     return render_template("login.html")

@app.route("/admin")
def admin():
    users=User.query.all()
    return render_template ("admin.html",data=users)

@app.route("/auth", methods=["GET","POST"])
def auth():
    if request.method=="POST":
        mail = request.form.get("name") # i will get my email entered in the webpage
        passw = request.form.get("pwd")
        u = User.query.get(mail)
        #select * from user where email==mail  ===> email,password,timestamp
        if u != None:
            if passw == u.password :
            #     print ("your mail id is found")
                session["email"]=mail
                return redirect(url_for('userhome'))
            else:
                return "invalid password"
        else:
            return "No account associated with this password"



@app.route("/home")
def userhome():
    try:
        user = session['email']
        return render_template("login.html",username = user,message="Sucessfully logged in : welcome!!")
    except:    
        return redirect(url_for('index'))

@app.route("/search",methods=["POST","GET"])
def search():
    try:
        username = session['email']
        if request.method=="POST":
            if not request.form.get("book"):
                return render_template("login.html",msg = "please search a book by its title or isbn or author or year",username=username)
            book = request.form.get("book")
            bookreq = str(book)
            booksdata = db.session.query(books.isbn,books.title,books.author,books.year).filter(or_(books.title.like("%"+bookreq+"%"),books.author.like("%"+bookreq+"%"),books.isbn.like("%"+bookreq+"%"),books.year.like("%"+bookreq+"%"))).all()
            if booksdata.__len__()==0:
                return render_template("login.html",msg = "we could not find books with your search!",username = username)
            else:
                return render_template("login.html",books=booksdata,username=username)
    except:
        return redirect(url_for('index'))

@app.route("/bookpage/<isbn>",methods=["POST","GET"])
def bookspage(isbn):
    try:
        
        username = session['email']
        book = db.session.query(books).filter(books.isbn==isbn).first()
        allreviews = review.query.filter_by(isbn=isbn).all()
        res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "2VIV9mRWiAq0OuKcOPiA", "isbns": book.isbn})
        data = res.text
        parsed = json.loads(data)
        print(parsed)
        res = {}
        for i in parsed:
            for j in (parsed[i]):
                res = j
        if request.method == "POST":
            rating = request.form.get("rating")
            reviews = request.form.get("review")
            isbn = book.isbn
            timestamp = time.ctime(time.time())
            title = book.title
            user = review(isbn=isbn, review=reviews, rating=rating,
                        time_stamp=timestamp, title=title, username=username)
            db.session.add(user)
            db.session.commit()
            # Get all the reviews for the given book.
            allreviews = review.query.filter_by(isbn=isbn).all()
            return render_template("review.html", book=book, review=allreviews, property="none", res=res,message="You reviewed this book!!")
        else:
            # database query to check if the user had given review to that paticular book.
            rev = review.query.filter(
                review.isbn == book.isbn, review.username == username).first()
            # if review was not given then dispaly the book page with review button
            if rev is None:
                return render_template("review.html", book=book, review=allreviews,res=res, username=username)
            else:
                return render_template("review.html", book=book, message="You reviewed this book!!", review=allreviews,res=res,property="none",username=username)
    except Exception as e:
        print(e)
        return redirect(url_for('index'))


@app.route("/logout",methods=["GET","POST"])
def logout():
    session["email"]=None
    return redirect("/register")

with app.app_context():
    main()