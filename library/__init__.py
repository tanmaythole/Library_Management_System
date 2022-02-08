from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST_NAME}/{DB_NAME}'

db = SQLAlchemy(app)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = SECRET_KEY


from . import routes
from . import models

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
login_manager.login_message_category = 'error'

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))