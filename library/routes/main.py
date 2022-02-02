from flask import Blueprint, get_flashed_messages, render_template, request
from flask_login import login_required
from library.models import Books, Members, Transactions
import math


main = Blueprint('main', __name__)

# dashboard
@main.route('/')
@login_required
def dashboard():
    get_flashed_messages()
    params = {"members_count":len(Members.query.all()), "books_count":len(Books.query.all())}
    return render_template("dashboard.html", params=params)


# Transaction
@main.route('/transactions')
@login_required
def transactions():
    get_flashed_messages()
    rows_per_page = 20
    transactions = Transactions.query.order_by(Transactions.isClosed.asc()).all()
    length = len(transactions)

    last = math.ceil(length/rows_per_page)

    page = request.args.get('page')
    page = 1 if not str(page).isnumeric() else int(page)

    transactions = transactions[(page-1)*rows_per_page : page*rows_per_page]
    if page > 1:
        prev = '?page='+str(page-1)
    else:
        prev = '#'
    if page < last:
        next = '?page='+str(page+1)
    else:
        next = '#'

    pagination_msg = {
            "total":length, 
            "start":(page-1)*rows_per_page + 1, 
            "end": page*rows_per_page if page*rows_per_page < length else length
        }
    return render_template("transactions.html", transactions=transactions, prev=prev, next=next, pagination_msg=pagination_msg)


# Reports
@main.route('/reports')
@login_required
def reports():
    books = Books.query.order_by(Books.average_rating.desc()).limit(10).all()
    members = Members.query.order_by(Members.amount_spent.desc()).limit(10).all()
    return render_template("reports.html", books=books, members=members)
