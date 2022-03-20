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


@app.route("/order", methods=["GET", "POST"])
def order():
    """Show order details"""
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
        
        # User if not logged in
        else:
            return render_template("order.html")
    
    # If route reached by "POST"
    elif request.method == "POST":
        
        # Initiate variable that will store the total value of transaction
        transaction_total = 0
        
        # Request data from the order form
        postage_price = float(request.form['postage'])
        print(f"Postage price: {postage_price}")
        transaction_total += postage_price
        postage = Postage.query.filter_by(postage_price=postage_price).first()
        postage_id = postage.id
        
        payment_type = request.form["payment"]
        print(f"Payment type: {payment_type}")
        payment = Payment.query.filter_by(payment_type=payment_type).first()
        payment_id = payment.id

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
            print(company_name)
        # User chose to log in now through login form in modal
        elif request.form.get("login_password"):                
            # Ensure email_address was submitted
            try:
                email_address = request.form.get("email-address")
            except AttributeError:
                print("Email not submitted")
                return apology("Podaj address email, który podałeś przy rejestracji", 400)
            
            # Ensure password was submitted
            try:
                password = request.form.get("password")
            except AttributeError:
                print("Password not submitted")
                return apology("Podaj hasło", 400)
        
            # Query database for email_address and check password  
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
            if user.comapny:
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
        order_ = Orders.query.filter_by(transaction_total=transaction_total, email=user_email, created=today()).first()
        order_id = order_.id
        
        # Add row to Realization table in db
        if request.form.get("extra-postage-info"):
            postage_info = request.form.get("extra-postage-info")
            realization = Realization(order_id=order_id, postage_info=postage_info)
        else:
            realization = Realization(order_id=order_id)
        db.session.add(realization)
        db.session.commit()     

        # Data received through Ajax request
        try:
            data = json.loads(request.data)
            #print(data)
        except:
            print("Ajax no respose")    

        # Loop through Ajax data
        for data_item_keys, data_item_values in data.items():
                     
            #if data_item_keys == "postageData":
                #postage_price = float(data["postageData"])
                #transaction_total += postage_price
                #postage = Postage.query.filter_by(postage_price=postage_price).first()
                #postage_id = postage.id
                 
            if data_item_keys == "cartTotalValueData":
                cart_value = float(data["cartTotalValueData"])
                transaction_total += cart_value 
            
            elif data_item_keys == "cartData":
              
                for cart_item in data_item_values:
                    print(cart_item) 
                    
                    for cart_item_key, cart_item_value in cart_item.items():

                        product_name = cart_item["productName"]
                        content_color = cart_item["contentColor"]
                        case_color = cart_item["caseColor"]
                        product_price = cart_item["productTotalPrice"]
                
                    # Adds all items from Ajax dict's cartData dict whose keys start with "line" to a lines_list
                    lines_list = [val for key, val in cart_item.items() if key.startswith("line")]
                        
                    # Creates a list of 9 elements ready to populate Content table in db
                    c_list = []
                    for num in range(9):
                        try:
                            line = lines_list[num]
                            #print(line)
                            c_list.append(line)
                        except IndexError:
                            line = "----"
                            #print(line)
                            c_list.append(line)
                    jsonify('success')
                    print(c_list)
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

                    order_product = Cart(product_id=product_id, content_id=content_id, content_color_id=content_color_id, case_color_id=case_color_id, price=product_price)
                    db.session.add(order_product)
                    db.session.commit()               
        
        flash("Dziękujemy za zamówienie!")
        return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        """Register user in database"""
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


