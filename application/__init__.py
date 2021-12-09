from flask import Flask,redirect
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager




application = Flask(__name__)
application.config['SECRET_KEY'] = '9814250305d2a591d904e59920907d35'
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(application)
bcrypt = Bcrypt(application)
login_manager = LoginManager(application)





from application import routes