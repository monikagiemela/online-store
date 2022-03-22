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


@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    """Change password"""

    if request.method == "GET":
        return render_template("password.html")
    # If user entered a new password the following checks if user entered a valid format of a password
    elif request.method == "POST":
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        if new_password != confirmation:
            return apology("Hasło wpisane w obu polach musi być identyczne", 400)
        elif len(new_password) < 8:
            return apology("Hasło powinno zawierac min. 8 znaków", 400)
        elif not re.search("[0-9]", new_password):
            return apology("Hasło powinno zawierać min. 1 cyfrę", 400)
        elif not re.search("[A-Z]", new_password):
            return apology("Hasło powinno zawierań min. 1 wielką literę", 400)
        elif not re.search("[a-z]", new_password):
            return apology("Hasło powinno zawierać min. 1 małą literę", 400)
        elif not re.search("[!@#$%^&*()-_]", new_password):
            return apology("Hasło powinno zawierać znak specjalny", 400)

        # Updates database 
        #db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(
            #new_password, method='pbkdf2:sha256', salt_length=8), id)

        flash("Twoje hasło zostało zmienione")
        
        return redirect("/user")