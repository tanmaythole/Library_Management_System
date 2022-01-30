from datetime import datetime
from flask import redirect, request
from .models import Books, Members, Transactions
from . import app, render_template, db
import requests

@app.route('/')
def dashboard():
    return render_template("dashboard.html")

@app.route('/books')
def books():
    books = Books.query.all()
    return render_template("books.html", books=books)

@app.route('/books/import', methods=['POST', 'GET'])
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
            
        return redirect("/books")

    return render_template("importBooks.html")


@app.route('/books/add', methods=['POST', 'GET'])
@app.route('/books/edit/<int:id>', methods=['POST', 'GET'])
def addBook(id=0):
    if request.method=='POST':
        if id==0:
            # add book
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
            return redirect('/books')
        else:
            # edit book of id
            r = request.form
            Books.query.filter_by(id=id).update(dict(
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
                    quantity = r['quantity']))
            db.session.commit()
            return redirect('/books')
    
    if id==0:
        params = {"isNew":True}
    else:
        params = Books.query.all()[0]
    
    return render_template("addbook.html", params=params)


@app.route('/books/delete/<int:id>', methods=['DELETE', 'GET'])
def deleteBook(id):
    book = Books.query.filter_by(id=id).first()
    db.session.delete(book)
    db.session.commit()
    return redirect('/books')


@app.route('/members')
def members():
    members = Members.query.all()
    return render_template("members.html", members=members)

@app.route('/members/add', methods=['GET', 'POST'])
@app.route('/members/edit/<int:id>', methods=['GET', 'POST'])
def addMember(id=0):
    if request.method=='POST':
        if id==0:
            # add member
            r = request.form
            mem = Members(
                    name = r['name'],
                    email = r['email']
                )
            db.session.add(mem)
            db.session.commit()
            return redirect('/members')
        else:
            # edit member of id
            r = request.form
            Members.query.filter_by(id=id).update(dict(name=r['name'], email=r['email']))
            db.session.commit()
            return redirect('/members')
    
    if id==0:
        params = {"isNew":True}
    else:
        params = Members.query.filter_by(id=id)[0]
    
    return render_template('addmember.html', params=params)


@app.route('/members/delete/<int:id>', methods=['DELETE', 'GET'])
def deleteMember(id):
    mem = Members.query.filter_by(id=id).first()
    db.session.delete(mem)
    db.session.commit()
    return redirect('/members')

@app.route('/transactions')
def transactions():
    transactions = Transactions.query.all()
    return render_template("transactions.html", transactions=transactions)

@app.route('/issue-book', methods=['GET', 'POST'])
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
            else:
                print("Books Not Available")
        else:
            print(f"Book not found to {form['book']} id.")
        return redirect('/transactions')
    return render_template('issueBook.html')

@app.route('/books/return/<int:id>', methods=['GET', 'POST'])
def returnBook(id):
    transaction = Transactions.query.filter_by(id=id).first()

    if transaction is None:
        return redirect('/transactions')

    book = Books.query.filter_by(id=transaction.book_id).first()
    member = Members.query.filter_by(id=transaction.member_id).first()

    total_no_of_days = (datetime.now() - transaction.issued_on).days
    total_no_of_days = total_no_of_days+1 if total_no_of_days==0 else total_no_of_days

    total_charge = total_no_of_days * transaction.per_day_fee

    if request.method=='POST':
        form = request.form

        debt = total_charge - int(form['amount_paid'])

        if member.outstanding_debt + debt < 500:
            transaction.returned_on = datetime.now()
            transaction.total_charge = total_charge
            transaction.amount_paid = int(form['amount_paid'])
            transaction.isClosed = True
            db.session.commit()

            member.outstanding_debt += debt
            member.amount_spent = int(form['amount_paid'])
            db.session.commit()

            book.available_books += 1
            book.issued_books -= 1
            db.session.commit()

            return redirect('/transactions')
        else:
            print('OutStanding Debt is more than 500')


    return render_template("returnBook.html", book=book, transaction=transaction, member=member, params={"total_no_of_days":total_no_of_days, "total_charge":total_charge})

@app.route('/popular-books')
def popularBooks():
    books = Books.query.order_by(Books.average_rating.desc()).limit(10).all()
    return render_template("mostPopularBooks.html", books=books)

@app.route('/highest-paying-customers')
def highestPayingCustomers():
    members = Members.query.order_by(Members.amount_spent.desc()).limit(10).all()
    return render_template("highestPayingCustomers.html", members=members)
