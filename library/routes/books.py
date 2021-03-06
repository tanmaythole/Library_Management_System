from datetime import datetime
from flask import Blueprint, flash, get_flashed_messages, redirect, render_template, request
from flask_login import login_required
from library import db
from library.models import Books, Members, Transactions
import math
import requests


books_ = Blueprint('books', __name__)

# Display Books
@books_.route('/books')
@login_required
def books():
    get_flashed_messages()
    rows_per_page = 15
    books = Books.query.all()

    length = len(books)
    last = math.ceil(length/rows_per_page)

    page = request.args.get('page')
    page = 1 if not str(page).isnumeric() else int(page)

    books = books[(page-1)*rows_per_page : page*rows_per_page]
    
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

    return render_template("books.html", books=books, prev=prev, next=next, pagination_msg=pagination_msg)

# Import Books
@books_.route('/books/import', methods=['POST', 'GET'])
@login_required
def import_books():
    if request.method=='POST':

        form = request.form
        url = 'https://frappe.io/api/method/frappe-library'
        params = {'page':1}

        if form['title']:
            params['title'] = form['title']
        elif form['authors']:
            params['authors'] = form['authors']
        elif form['isbn']:
            params['isbn'] = form['isbn']
        elif form['publisher']:
            params['publisher'] = form['publisher']

        books_added = 0
        
        while books_added != int(form['no_of_books']):
            res = requests.get(url, params=params).json()

            if not res['message']:
                break

            for book in res['message']:
                
                if Books.query.filter_by(isbn=book['isbn']).first():
                    continue
                
                b = Books(
                        title=book['title'],
                        authors=book['authors'],
                        average_rating=book['average_rating'],
                        isbn=book['isbn'],
                        isbn13=book['isbn13'],
                        language=book['language_code'],
                        num_pages=book['  num_pages'],
                        ratings_count=book['ratings_count'],
                        pub_date=datetime.strptime(book['publication_date'], '%M/%d/%Y').date(),
                        publisher=book['publisher'],
                        quantity=form['quantity_per_books'],
                        available_books=form['quantity_per_books'],
                        issued_books=0
                    )
                db.session.add(b)
                db.session.commit()
                books_added += 1

                if books_added == int(form['no_of_books']):
                    break
            
            params['page'] += 1
            
        if books_added == int(form['no_of_books']):
            flash(f"{books_added}/{form['no_of_books']} books added successfully.", 'success')
        elif books_added==0:
            flash(f"New books NOT found for given parameters", 'error')
        else:
            flash(f"{books_added}/{form['no_of_books']} books are added successfully.", 'warning')

        return redirect("/books")

    return render_template("importBooks.html")

# Add/Edit Books
@books_.route('/books/add', methods=['POST', 'GET'])
@books_.route('/books/edit/<int:id>', methods=['POST', 'GET'])
@login_required
def addBook(id=0):
    if id==0:
        params = {"isNew":True}
    else:
        params = Books.query.filter_by(id=id).first()

    if request.method=='POST':
        if id==0:
            # add book
            try:
                r = request.form
                b = Books(
                        title=r['title'],
                        authors = r['authors'],
                        average_rating = r['average_rating'],
                        isbn = r['isbn'],
                        isbn13 = r['isbn13'],
                        language = r['language'],
                        num_pages = r['num_of_pages'],
                        ratings_count = r['ratings_count'],
                        pub_date = r['publication_date'],
                        publisher = r['publisher'],
                        quantity = r['quantity'],
                        available_books = r['quantity'],
                        issued_books = 0
                    )
                db.session.add(b)
                db.session.commit()
                flash(f'Book {b.title} Added Successfully!!', 'success')
                return redirect('/books')
            except Exception as e:
                flash(f'Something went wrong while adding the book - {e}', 'error')
                return render_template("addbook.html", params={params})
        else:
            # edit book of id
            try:
                r = request.form
                b = Books.query.filter_by(id=id)

                b.title=r['title']
                b.authors = r['authors']
                b.average_rating = r['average_rating']
                b.isbn = r['isbn']
                b.isbn13 = r['isbn13']
                b.language = r['language']
                b.num_pages = r['num_of_pages']
                b.ratings_count = r['ratings_count']
                b.pub_date = r['publication_date']
                b.publisher = r['publisher']
                b.quantity = r['quantity']
                b.available_books = int(r['quantity']) - b[0].issued_books
                
                
                db.session.commit()
                
                flash(f'Book {b.title} Updted Successfully!!', 'success')
                return redirect('/books')
            except Exception as e:
                flash(f'Something went wrong while updating the book - {e}', 'error')
                return render_template("addbook.html", params={params})

    return render_template("addbook.html", params=params)

# Delete Books
@books_.route('/books/delete/<int:id>', methods=['DELETE', 'GET'])
@login_required
def deleteBook(id):
    try:
        book = Books.query.filter_by(id=id).first()
        db.session.delete(book)
        db.session.commit()
        flash(f"Book deleted Successfully.", "success")
    except Exception as e:
        flash(f"Something Went Wrong - {e}", "error")
    return redirect('/books')


# Issue Book
@books_.route('/issue-book', methods=['GET', 'POST'])
@login_required
def issueBook():
    if request.method == 'POST':
        form = request.form
        
        isBookFound = Books.query.filter_by(id=form['book']).first()
        
        if isBookFound is not None:
            if isBookFound.available_books>0:
                transaction = Transactions(
                        book_id=form['book'],
                        member_id=form['member'],
                        per_day_fee=form['per_day_fee']
                    )
                db.session.add(transaction)
                db.session.commit()

                isBookFound.available_books=isBookFound.available_books-1, 
                isBookFound.issued_books=isBookFound.issued_books+1

                db.session.commit()

                flash(f"Book issued successfully.", "success")
            else:
                flash(f"Book with {form['book']} id not available.", "error")
        else:
            flash(f"Book not found to {form['book']} id.", "error")
        return redirect('/transactions')
    return render_template('issueBook.html')


# Return Book
@books_.route('/books/return/<int:id>', methods=['GET', 'POST'])
@login_required
def returnBook(id):
    transaction = Transactions.query.filter_by(id=id).first()

    if transaction is None:
        flash(f"Something Went Wrong.", 'error')
        return redirect('/transactions')

    book = Books.query.filter_by(id=transaction.book_id).first()
    member = Members.query.filter_by(id=transaction.member_id).first()

    total_no_of_days = (datetime.now() - transaction.issued_on).days
    total_no_of_days = total_no_of_days+1 if total_no_of_days==0 else total_no_of_days

    total_charge = total_no_of_days * transaction.per_day_fee

    if request.method=='POST':
        try:
            form = request.form

            debt = total_charge - int(form['amount_paid'])

            if member.outstanding_debt + debt < 500:
                transaction.returned_on = datetime.now()
                transaction.total_charge = total_charge
                transaction.amount_paid = int(form['amount_paid'])
                transaction.isClosed = True
                db.session.commit()

                member.outstanding_debt += debt
                member.amount_spent += int(form['amount_paid'])
                db.session.commit()

                book.available_books += 1
                book.issued_books -= 1
                db.session.commit()

                flash(f"Book returned successfully.", "success")
                return redirect('/transactions')
            else:
                flash(f"OutStanding Debt of member is more than 500.", "error")
        except Exception as e:
            flash(f"Something Went Wrong.", "error")


    return render_template("returnBook.html", book=book, transaction=transaction, member=member, params={"total_no_of_days":total_no_of_days, "total_charge":total_charge})


# Search Books
@books_.route('/search')
@login_required
def search():
    get_flashed_messages()
    rows_per_page = 10

    search_by = request.args['search_by']
    q = request.args['q']
    page = request.args.get('page')
    page = 1 if not str(page).isnumeric() else int(page)

    if search_by=='title':
        results = Books.query.filter(Books.title.like("%"+q+"%")).all()
    elif search_by=='authors':
        results = Books.query.filter(Books.authors.like("%"+q+"%")).all()
    elif search_by=='isbn':
        results = Books.query.filter_by(isbn=q).all()
    else:
        return redirect('/')

    length = len(results)
    last = math.ceil(length/rows_per_page)

    results = results[(page-1)*rows_per_page : page*rows_per_page]

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
    return render_template('searchResults.html', results=results, prev=prev, next=next, pagination_msg=pagination_msg)
    