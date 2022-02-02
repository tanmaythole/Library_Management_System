from flask import Blueprint, flash, redirect, render_template, request
from flask_login import current_user, login_required, login_user, logout_user
from library.models import User
from . import db
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')

    if request.method=='POST':
        r = request.form
        remember = True if request.form.get('remember') else False
        
        user = User.query.filter_by(email=r['email']).first()
        
        if user and check_password_hash(user.password, r['password']):
            login_user(user, remember=remember)

            next = request.args.get('next')
            if not next:
                next = '/'
            return redirect(next)

        flash(f"Invalid Credentials!!", "error")
    return render_template("login.html")


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')