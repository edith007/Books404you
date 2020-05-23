from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    username = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)

class Book(db.Model):
    __tablename__ = "books"
    book_id = db.Column(db.Integer, primary_key = True)
    isbn = db.Column(db.String, nullable = False)
    title = db.Column(db.String, nullable = False)
    author = db.Column(db.String, nullable = False)
    year = db.Column(db.String, nullable = False)

class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)
    rating = db.Column(db.Integer, nullable = True)
    comment = db.Column(db.String, nullable = True)