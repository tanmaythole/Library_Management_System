from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://tanmay:Pass1234@localhost/libraryms'

db = SQLAlchemy(app)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


from . import routes
from . import models

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
login_manager.login_message_category = 'error'

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))