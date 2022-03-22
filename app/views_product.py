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


@app.route("/product", methods=["GET"])
def product():
    """Show all product page"""
    product_id = request.args.get("id")

    # Fetch product details from database
    product = Products.query.filter_by(id=product_id).first()
    product_name = product.product_name
    product_symbol = product.symbol
    print_size = product.print_size
    max_lines = product.max_lines
    product_price = product.price
    product_description = product.description
    brand_id = product.brand_id
    brand_name = Brands.query.filter_by(id=brand_id)

    if product.availability > 0:
        product_availability = "Dostępny"

    case_colors = Casecolors.query.all()

    case_colors_list = []
    for case_color in case_colors:
        case_colors_list.append(case_color.case_color_name)
    
    content_colors = Contentcolors.query.all()
    content_colors_list = []
    for content_color in content_colors:
        content_colors_list.append(content_color.content_color_name)

    """ Fetch file if user uploaded it """
    if 'order_file' in request.files:
        file = request.files['order_file']  
        filename = secure_filename(file.filename)  
        if file.filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['ALLOWED_EXTENSIONS']: 
                apology("Zły plik", 400)

            session["file"] = filename
            file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    
    return render_template("product.html", product_name=product_name, 
    product_availability=product_availability, product_symbol=product_symbol, 
    print_size=print_size, max_lines=max_lines, product_price=product_price,
    product_description=product_description,content_colors_list=content_colors_list,
    case_colors_list=case_colors_list)