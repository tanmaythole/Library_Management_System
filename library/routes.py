from flask import request
from .models import Books, Members
from . import app, render_template

@app.route('/')
def dashboard():
    return render_template("dashboard.html")

@app.route('/books')
def books():
    books = Books.query.all()
    return render_template("books.html", books=books)

@app.route('/books/add')
@app.route('/books/edit/<int:id>')
def addBook(id=0):
    if request.method=='POST':
        if id==0:
            # add book
            pass
        else:
            # edit book of id
            pass
    
    if id==0:
        params = {}
    else:
        params = {"title":"The Wings of Fire"}
    
    return render_template("addbook.html", params=params)


@app.route('/books/delete/<int:id>')
def deleteBook():
    pass

@app.route('/members')
def members():
    members = Members.query.all()
    return render_template("members.html", members=members)

@app.route('/members/add')
@app.route('/members/edit/<int:id>')
def addMember(id=0):
    if request.method=='POST':
        if id==0:
            # add member
            pass
        else:
            # edit member of id
            pass
    
    if id==0:
        params = {}
    else:
        params = {"name":"name"}
    
    return render_template('addmember.html', params=params)


@app.route('/members/delete/<int:id>')
def deleteMember():
    pass

@app.route('/transactions')
def transactions():
    pass

@app.route('/most-popular-books')
def popularBooks():
    pass

@app.route('/highest-paying-customers')
def highestPayingCustomers():
    pass
