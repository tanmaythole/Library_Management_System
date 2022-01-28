from . import app, render_template

@app.route('/')
def dashboard():
    return render_template("dashboard.html")

@app.route('/books')
def books():
    pass

@app.route('/books/add')
def addBook():
    pass

@app.route('/books/edit/<int:id>')
def editBook():
    pass

@app.route('/books/delete/<int:id>')
def deleteBook():
    pass

@app.route('/members')
def members():
    pass

@app.route('/members/add')
def addMember():
    pass

@app.route('/members/edit/<int:id>')
def editMember():
    pass

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
