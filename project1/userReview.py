from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class review(db.Model):
    __tablename__ = "reviews"
    isbn = db.Column(db.String, nullable=False, primary_key=True)
    title = db.Column(db.String, nullable=False)
    rating = db.Column(db.String, nullable=False)
    review = db.Column(db.String, nullable=False)
    time_stamp = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, primary_key=True)