# import csv
# import os
# from flask import Flask, render_template, request
# from imports import *

# # Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")

# app = Flask(__name__)

# # Configure session to use filesystem
# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# print( os.getenv("DATABASE_URL"))
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SESSION_TYPE"]="filesystem"
# # Session(app)

# db.init_app(app)


# def main():
#     db.create_all()
#     a = "C:\\Users\\91970\\Desktop\\IT\\java\\SAD-2019501084\\project1\\books.csv"
#     f = open(a)
#     reader = csv.reader(f)
#     # next(reader)
    

#     for isbn, title, author, year in reader:
#         book = books(isbn=isbn, title=title, author=author, year=year)
#         db.add(book)
#         print(
#             f"added{book.title} with number {book.isbn} written by {book.author} published in the year {book.year}")
#     db.commit()
#     print("commited")


# # if __name__ == "__main__":
# with app.app_context():
#     main()
from datetime import datetime as dt
import os
from flask import Flask, session,request,render_template,flash,logging,redirect,url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
import csv
from models import *
from imports import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)




def main():
    db.create_all()
    a = "C:\\Users\\91970\\Desktop\\IT\\java\\SAD-2019501084\\project1\\books.csv"
    f = open(a)
    reader = csv.reader(f)
    for isbn,title,author,year in reader:
        book = books(isbn=isbn, title=title, author=author,year=year)
        db.session.add(book)
        print(f"Added book of year {year} ,isbn: {isbn},title: {title} ,author: {author}.")
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        main()