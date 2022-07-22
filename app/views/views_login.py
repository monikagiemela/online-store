from app import app
from app.models import Users
from app.helpers import apology
from flask import flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure email_address was submitted
        try:
            email_address = request.form.get("login-email-address")            
        except AttributeError:
            return apology("Podaj address email, który podałeś przy rejestracji", 400)
        
        # Ensure password was submitted
        try:
            password = request.form.get("login-password")         
        except AttributeError:
            return apology("Podaj hasło", 400)
        
        # Query database for email_address and check password  
        user = None
        try:
            user = Users.query.filter_by(email_address=email_address).first() 
        except AttributeError:
            return apology("Nieprawidłowy adres email lub hasło", 400)

        try: 
            check_password_hash(user.hash, password)
        except AttributeError:        
            return apology("Nieprawidłowy adres email lub hasło", 400)

        # Remember which user has logged in
        user_id = user.id
        session["user_id"] = user_id
        flash('Zostałeś zalogowany')
        # Redirect user to home page
        return redirect("/")

        # User reached route via GET
    else:
        return render_template("login.html")