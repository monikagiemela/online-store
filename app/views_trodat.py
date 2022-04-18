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


@app.route("/trodat", methods=["GET"])
def trodat():
    """Show all Trodat products page"""
    
    # Fetch product details from database
    products = Products.query.filter_by(brand_id=1).all()

    for product in products:
        product_name = product.product_name
        print(product_name)
        product_symbol = product.symbol
        print_size = product.print_size
        max_lines = product.max_lines
        product_price = product.price
        product_description = product.description
        brand_id = product.brand_id
        brand_name = Brands.query.filter_by(id=brand_id)
    return render_template("trodat.html", products=products)
