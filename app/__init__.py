import os
from os.path import join, dirname, realpath
from dotenv import load_dotenv 

from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from app.helpers import absolute, PLN

load_dotenv()

# Configure application
app = Flask(__name__)
SECRET_KEY = os.environ.get('SECRET_KEY')
app.config["SECRET_KEY"] = SECRET_KEY


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure file upload folder
app.config['UPLOAD_PATH'] = 'app/uploads'
app.config['ALLOWED_EXTENSIONS'] = ['txt', 'pdf', 'png', 'jpg', 'jpeg', '.doc', '.docx']

# Custom filters
app.jinja_env.filters["PLN"] = PLN
app.jinja_env.filters["absolute"] = absolute
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///store.db'
db = SQLAlchemy(app)

from app import views
from app.views_order import order
from app.views_password import password
from app.views_product import product
from app.views_login import login
from app.views_register import register
from app.views_trodat import trodat
from app import models






