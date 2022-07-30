import os
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate

from app.helpers import absolute, PLN


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

# Configure email services
# Requires that "Less secure app access" be on
# https://support.google.com/accounts/answer/6010255
app.config["MAIL_DEFAULT_SENDER"] = os.environ["SENDER_EMAIL"]
app.config["MAIL_PASSWORD"] = os.environ["MAIL_PWD"]
app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ["SENDER_EMAIL"]
mail = Mail(app)

# Custom filters
app.jinja_env.filters["PLN"] = PLN
app.jinja_env.filters["absolute"] = absolute
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///store.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.models import *
from app.views.views import after_request, index, all, colop, wagraf, logout, user
from app.views.views_order import order
from app.views.views_password import password
from app.views.views_product import product
from app.views.views_login import login
from app.views.views_register import register
from app.views.views_category_all import trodat



"""
# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
    from_email='from_email@example.com',
    to_emails='to@example.com',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)

"""