import os
import sys
from flask import Flask, session,request,render_template,flash,logging,redirect,url_for
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
from models import User,db
import time
from userReview import *
from test import bookreview
from sqlalchemy import create_engine,desc
import json
import requests


app = Flask(__name__, static_url_path='/static')

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

@app.route("/login",methods=["GET","POST"])
def login():
    return render_template("login.html")

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
                return render_template("account.html")
            else:
                return "invalid password"
        else:
            return "No account associated with this password"

@app.route("/search",methods=["GET"])
def search():
    if session["email"] == None:
        return redirect(url_for("/logout"))
    else:
        return "Maintained successfully"

@app.route("/logout",methods=["GET","POST"])
def logout():
    session["email"]=None
    return redirect("/register")

@app.route("/bookpage",methods=["POST","GET"])
def bookrev():
    book = bookreview("1416949658", "The Dark Is Rising", "Susan Cooper", 1973)
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "2VIV9mRWiAq0OuKcOPiA", "isbns": book.isbn})
    data = res.text
    parsed = json.loads(data)
    print(parsed)
    res = {}
    for i in parsed:
        for j in (parsed[i]):
            res = j

    # Variables for testing
    bookisbn = book.isbn
    usernam = "rishabh"

    # Get all the reviews for the given book.
    allreviews = review.query.filter_by(isbn=bookisbn).all()
    if request.method == "POST":
        rating = request.form.get("rating")
        reviews = request.form.get("review")
        isbn = book.isbn
        timestamp = time.ctime(time.time())
        title = book.title
        username = "rishabh"
        user = review(isbn=isbn, review=reviews, rating=rating,
                      time_stamp=timestamp, title=title, username=username)
        db.session.add(user)
        db.session.commit()


        # Get all the reviews for the given book.
        allreviews = review.query.filter_by(isbn=bookisbn).all()
        return render_template("review.html", res=res, book=book, review=allreviews, property="none", message="You reviewed this book!!")
    else:
        # database query to check if the user had given review to that paticular book.
        rev = review.query.filter(
            review.isbn == bookisbn, review.username == usernam).first()

        # print(rev)

        # if review was not given then dispaly the book page with review button
        if rev is None:
            return render_template("review.html", book=book, review=allreviews, res=res)
        else:
            return render_template("review.html", book=book, message="You reviewed this book!!", review=allreviews, res=res, property="none")




# if __name__ == "__main__":
with app.app_context():
    main()