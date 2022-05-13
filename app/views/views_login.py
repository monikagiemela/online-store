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


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure email_address was submitted
        try:
            email_address = request.form.get("email-address")
        except AttributeError:
            return apology("Podaj address email, który podałeś przy rejestracji", 400)
        
        # Ensure password was submitted
        try:
            password = request.form.get("password")
        except AttributeError:
            return apology("Podaj hasło", 400)
       
        # Query database for email_address and check password  
        try:
            user = Users.query.filter_by(email_address=email_address).first()
        except AttributeError:
            return apology("Nieprawidłowy adres email lub hasło", 400)
            
        try:
            check_password_hash(user.hash, password)
        except:
            return apology("Nieprawidłowy adres email lub hasło", 400)
        
        # Remember which user has logged in
        session["user_id"] = user.id

        flash('Zostałeś zalogowany')
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("login.html")