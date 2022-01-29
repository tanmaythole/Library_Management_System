from flask import redirect, request
from .models import Books, Members
from . import app, render_template, db

@app.route('/')
def dashboard():
    return render_template("dashboard.html")

@app.route('/books')
def books():
    books = Books.query.all()
    return render_template("books.html", books=books)

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
    pass

@app.route('/most-popular-books')
def popularBooks():
    pass

@app.route('/highest-paying-customers')
def highestPayingCustomers():
    pass
