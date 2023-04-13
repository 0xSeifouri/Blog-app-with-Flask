from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'e0c8638fb6f650276907a544d6a2ad9bc5c373582ea372c7845e013f910caca0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.sqlite3'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# with app.app_context():
#     db.create_all()

from .routes import home

