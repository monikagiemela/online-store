import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename




def absolute(quantity):
    """Format value as absolute"""
    if quantity < 0:
        return quantity * (-1)
    return quantity

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def PLN(value):
    """Format value as zł."""
    return f"{value:,.2f} zł"


"""def registration():
    Register user in database
    user_name = request.form.get("user-name")
    user_lastname = request.form.get("user-lastname")
    user_email = request.form.get("user-email-address")

    user_password = request.form.get("user-password")
    hash = generate_password_hash(user_password, method='pbkdf2:sha256', salt_length=8)
        
    user_street = request.form.get("user-street")
    user_house_number = request.form.get("user-house-number")
    
    user_city = request.form.get("user-city")
    user_postcode = request.form.get("user-postcode")
    user_country = request.form.get("user-country")
    user_phone = request.form.get("user-phone") 
    
    if request.form.get("user-apertment-number"):
        user_apartment_number = request.form.get("user-apertment-number")
        postage_address = f"{user_street} {user_house_number}/{user_apartment_number}"
    else:
        postage_address = f"{user_street} {user_house_number}"
    
    if request.form.get("company-name") and request.form.get("nip"):
        company_name = request.form.get("company-name")
        nip = request.form.get("nip")

    # Add user details to Users table in db    
    user = Users(first_name=user_name, last_name=user_lastname, company=company_name, nip=nip, email_address=user_email, hash=hash, phone=user_phone, address=postage_address, post_code=user_postcode, city=user_city, country=user_country)
    return user"""
  
