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


@app.route("/order", methods=["GET", "POST"])
def order():
    """Show order details and finalize the order"""
    if request.method == "GET":
        # User is already logged in
        if session.get("user_id"):
            id = session.get("user_id")

            # Fetch user data from db
            user = Users.query.filter_by(id=id).first()
            user_name = user.first_name
            user_lastname = user.last_name
            user_email = user.email_address  
            user_phone = user.phone
            postage_address = user.address
            user_postcode = user.post_code
            user_city = user.city
            user_country = user.country
            if user.company:
                company_name = user.company
                nip = user.nip
            else:
                company_name = None
                nip = None
            
            session_ = "in_session"

            return render_template("order.html", user_name=user_name, user_lastname=user_lastname, user_email=user_email, user_phone=user_phone, postage_address=postage_address, user_postcode=user_postcode, user_city=user_city, user_country=user_country, company_name=company_name, nip=nip, session_=session_)
        
        # User is not logged in
        else:
            return render_template("order.html")
    
    # Route reached by "POST"
    elif request.method == "POST":

        # Initiate variable that will store the total value of transaction
        #transaction_total = 0
        
        # Request data from the order form
        #postage_price = float(request.form['postage'])
        #print(f"Postage price: {postage_price}")
        #transaction_total += postage_price
        #postage = Postage.query.filter_by(postage_price=postage_price).first()
        #postage_id = postage.id
        
        #payment_type = request.form["payment"]
        #print(f"Payment type: {payment_type}")
        #payment = Payment.query.filter_by(payment_type=payment_type).first()
        #payment_id = payment.id

        # User is logged in
        if session.get("user_id"):
            id = session.get("user_id")
        
            # Fetch user data from Users table in db
            user = Users.query.filter_by(id=id).first()
            user_name = user.first_name
            user_lastname = user.last_name
            user_email = user.email_address  
            user_phone = user.phone
            postage_address = user.address
            user_postcode = user.post_code
            user_city = user.city
            user_country = user.country
            if user.company:
                company_name = user.company
                nip = user.nip
            else:
                company_name = None
                nip = None
        
        # User chose to log in now through login form in modal
        elif request.form.get("login-password"):                
            
            # Ensure email_address was submitted
            try:
                email_address = request.form.get("login-email-address")
            except AttributeError:
                print("Email not submitted")
                return apology("Podaj address email, który podałeś przy rejestracji", 400)
            
            # Ensure password was submitted
            try:
                password = request.form.get("login-password")
            except AttributeError:
                print("Password not submitted")
                return apology("Podaj hasło", 400)
        
            # Query database for email_address and check password  
            user = None
            try:
                user = Users.query.filter_by(email_address=email_address).first()
            except AttributeError:
                print("Email not in db")
                return apology("Nieprawidłowy adres email lub hasło", 400)
                
            try:
                check_password_hash(user.hash, password)
            except:
                print("Wrong password")
                return apology("Nieprawidłowy adres email lub hasło", 400)
        
            # Remember which user has logged in
            session["user_id"] = user.id
            
            # Fetch user data from db
            user_name = user.first_name
            user_lastname = user.last_name
            user_email = user.email_address   
            user_phone = user.phone
            postage_address = user.address
            user_postcode = user.post_code
            user_city = user.city
            user_country = user.country
            if user.company:
                company_name = user.company
                nip = user.nip
            else:
                company_name = "individual"
                nip = "individual"
            
            session_ = "in_session"
            
            return render_template("order.html", user_name=user_name, user_lastname=user_lastname, user_email=user_email, user_phone=user_phone, postage_address=postage_address, user_postcode=user_postcode, user_city=user_city, user_country=user_country, company_name=company_name, nip=nip, session_=session_)

        # User is not registered 
        else:
            user_name = request.form.get("user-name")
            user_lastname = request.form.get("user-lastname")
            user_email = request.form.get("user-email-address")
            
            user_password = ''
            hash = ''
            if request.form.get("user-password"):
                user_password = request.form.get("user-password")
                hash = generate_password_hash(user_password, method='pbkdf2:sha256', salt_length=8)
                
            user_street = request.form.get("user-street")
            user_house_number = request.form.get("user-house-number")
            
            user_city = request.form.get("user-city")
            user_postcode = request.form.get("user-postcode")
            user_country = request.form.get("user-country")
            user_phone = request.form.get("user-phone") 
            
            try:
                user_apartment_number = request.form.get("user-apartment-number")
                postage_address = f"{user_street} {user_house_number}/{user_apartment_number}"
            except:
                postage_address = f"{user_street} {user_house_number}"
            
            if request.form.get("company-name") and request.form.get("nip"):
                company_name = request.form.get("company-name")
                nip = request.form.get("nip")
                invoice = "yes"

            # If user chose to register, add user details to Users table in db
            if user_password: 
                if not request.form.get("company-name"):
                    user = Users(first_name=user_name, last_name=user_lastname, email_address=user_email, hash=hash, phone=user_phone, address=postage_address, post_code=user_postcode, city=user_city, country=user_country)
                
                else:
                    company_name = request.form.get("company-name")
                    nip = request.form.get("nip") 
                    user = Users(first_name=user_name, last_name=user_lastname, company=company_name, nip=nip, email_address=user_email, hash=hash, phone=user_phone, address=postage_address, post_code=user_postcode, city=user_city, country=user_country)
                
                db.session.add(user)
                db.session.commit()

        # Data received through Ajax request
        #data = None
        try:
            data = json.loads(request.data)
        except:
            print("Ajax no respose")      
        
        # Initiate variable that will store the total value of transaction
        transaction_total = 0
        cart_value = 0
        postage_id = 0
        payment_id = 0
        invoice = ''

        # Loop through Ajax data
        for data_item_keys, data_item_values in data.items():
                            
            if data_item_keys == "postageData":
                postage_price = float(data["postageData"])
                #print(f"Postage price: {postage_price}")
                transaction_total += postage_price
                postage = Postage.query.filter_by(postage_price=postage_price).first()
                postage_id = postage.id
                
            if data_item_keys == "paymentData":
                payment_type = data["paymentData"]
                #print(f"Payment type: {payment_type}")
                payment = Payment.query.filter_by(payment_type=payment_type).first()
                payment_id = payment.id     
                
            if data_item_keys == "cartTotalValueData":
                cart_value = float(data["cartTotalValueData"])
                transaction_total += cart_value 
            
        # Add row to Order table in db
        today = datetime.today()
        if id:
            user_order = Orders(transaction_total=transaction_total, cart_value=cart_value, postage_id=postage_id, first_name=user_name, lastname=user_lastname, email=user_email, phone=user_phone, address=postage_address, post_code=user_postcode, city=user_city, country=user_country, invoice=invoice, created=today, user_id=id, payment_id=payment_id)
        elif hash:
            user = Users.query.filter_by(hash=hash).first()
            user_id = user.id
            user_order = Orders(transaction_total=transaction_total, cart_value=cart_value, postage_id=postage_id, first_name=user_name, lastname=user_lastname, email=user_email, phone=user_phone, address=postage_address, post_code=user_postcode, city=user_city, country=user_country, invoice=invoice, created=today, user_id=user_id, payment_id=payment_id)
        else:
            user_order = Orders(transaction_total=transaction_total, cart_value=cart_value, postage_id=postage_id, first_name=user_name, lastname=user_lastname, email=user_email, phone=user_phone, address=postage_address, post_code=user_postcode, city=user_city, country=user_country, invoice=invoice, created=today, payment_id=payment_id)
        db.session.add(user_order)
        db.session.commit() 

        # Query db Orders table for order_id of the current order
        order_ = Orders.query.filter_by(transaction_total=transaction_total, email=user_email, created=today).first()
        order_id = order_.id

        # Add row to Realization table in db
        if request.form.get("extra-postage-info"):
            postage_info = request.form.get("extra-postage-info")
            print(postage_info)
            realization = Realization(order_id=order_id, postage_info=postage_info)
        else:
            realization = Realization(order_id=order_id)
        db.session.add(realization)
        db.session.commit() 

        for data_item_keys, data_item_values in data.items():

            if data_item_keys == "cartData":
            
                for cart_item in data_item_values:
                
                    for _ in cart_item.items():

                        product_name = cart_item["productName"]
                        content_color = cart_item["contentColor"]
                        case_color = cart_item["caseColor"]
                        product_price = cart_item["productTotalPrice"]
                
                    # Add all items from Ajax's cartData dict whose keys start with "line" to a lines_list
                    lines_list = [val for key, val in cart_item.items() if key.startswith("line")]
                        
                    # Create a list of 9 elements ready to populate Content table in db
                    c_list = []
                    for num in range(9):
                        try:
                            line = lines_list[num]
                            c_list.append(line)
                        except IndexError:
                            line = "----"
                            c_list.append(line)
                    jsonify('success')
            
                    # Add row to Content table in db
                    content_lines = Content(line_1=c_list[0], line_2=c_list[1], line_3=c_list[2], line_4=c_list[3], line_5=c_list[4], line_6=c_list[5], line_7=c_list[6], line_8=c_list[7], line_9=c_list[8])  
                    db.session.add(content_lines)
                    db.session.commit()

                    # Add row with details to Cart table in db
                    content_id = content_lines.id
                    product_ = Products.query.filter_by(product_name=product_name).first()
                    product_id = product_.id

                    content_color_ = Contentcolors.query.filter_by(content_color_name=content_color).first()
                    content_color_id = content_color_.id

                    case_color_ = Casecolors.query.filter_by(case_color_name=case_color).first()
                    case_color_id = case_color_.id
    
                    order_product = Cart(product_id=product_id, content_id=content_id, content_color_id=content_color_id, case_color_id=case_color_id, price=product_price, order_id=order_id)
                    db.session.add(order_product)
                    db.session.commit()

        flash("Dziękujemy za zamówienie!")
        return redirect("/")