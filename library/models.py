from datetime import datetime
from . import db

class Members(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    outstanding_debt = db.Column(db.Float, nullable=False, default=0.0)
    amount_spent = db.Column(db.Float, nullable=False, default=0.0)
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.now)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    authors = db.Column(db.String(255), nullable=False)
    average_rating = db.Column(db.Float, nullable=True)
    isbn = db.Column(db.String(10), nullable=False, unique=True)
    isbn13 = db.Column(db.String(13), nullable=False, unique=True)
    language = db.Column(db.String(3), nullable=False)
    num_pages = db.Column(db.Integer, nullable=False)
    ratings_count = db.Column(db.Integer, nullable=True)
    pub_date = db.Column(db.Date, nullable=False)
    publisher = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    available_books = db.Column(db.Integer, nullable=False)
    issued_books = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    per_day_fee = db.Column(db.Integer, nullable=False)
    issued_on = db.Column(db.DateTime, nullable=False, default=datetime.now())
    returned_on = db.Column(db.DateTime, nullable=True)
    total_charge = db.Column(db.Integer, nullable=True)
    amount_paid = db.Column(db.Integer, nullable=True)
    isClosed = db.Column(db.Boolean, nullable=False, default=False)
