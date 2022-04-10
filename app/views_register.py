from curses.ascii import NUL
from datetime import datetime
import os
import re


from app import app, db
from app.models import Brands, Cart, Categories, Casecolors, Content, Contentcolors, Invoices,  Orders, OrderProducts, Products,  Postage, Realization, Users, Payment
from app.helpers import apology, login_required, absolute, PLN


from flask import flash, redirect, render_template, request, session, jsonify, url_for
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import json


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        """Register user in database"""
        user_name = request.form.get("user-name")
        user_lastname = request.form.get("user-lastname")
        user_email = request.form.get("user-email-address")

        user_password = request.form.get("user-password")
        hash = generate_password_hash(user_password, method='pbkdf2:sha256', salt_length=16)
            
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
        
        # Add user details to Users table in db   
        if not request.form.get("company-name"):
            user = Users(first_name=user_name, last_name=user_lastname, email_address=user_email, hash=hash, phone=user_phone, address=postage_address, post_code=user_postcode, city=user_city, country=user_country)
        
        else:
            company_name = request.form.get("company-name")
            nip = request.form.get("nip") 
            user = Users(first_name=user_name, last_name=user_lastname, company=company_name, nip=nip, email_address=user_email, hash=hash, phone=user_phone, address=postage_address, post_code=user_postcode, city=user_city, country=user_country)

        db.session.add(user)
        db.session.commit()
        
        flash('Dziękujemy za rejestrację')
        return redirect("/login")

    else:
        return render_template("register.html")