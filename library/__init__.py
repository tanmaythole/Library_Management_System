from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://tanmay:Pass1234@localhost/libraryms'

db = SQLAlchemy(app)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

from . import routes
from . import models