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


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET"])
def index():
    """Show homepage with most popular products"""
    id = session.get("user_id")

    return render_template("index.html")


@app.route("/all", methods=["GET"])
def all():
    """Show all products"""
    return render_template("all.html")


@app.route("/colop", methods=["GET"])
def colop():
    """Show all Colop products"""
    return render_template("colop.html")


@app.route("/trodat", methods=["GET"])
def trodat():
    """Show all Trodat products"""
    return render_template("trodat.html")


@app.route("/wagraf", methods=["GET"])
def wagraf():
    """Show all Wagraf products"""
    return render_template("wagraf.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    flash('Zostałeś wylogowany')
    return redirect("/")


@app.route("/user", methods=["GET"])
@login_required
def user():
    """History of user transactions and account management"""

    if not session.get("user_id"):       
        return render_template("login.html")
    else:
        id = session.get("user_id")

        #SQL for user_transactions
             
        return render_template("user.html")



    







