from app import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False,autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    company = db.Column(db.Text, nullable=True)
    nip = db.Column(db.Text, nullable=True)
    email_address = db.Column(db.Text, unique=True, nullable=False)
    hash = db.Column(db.Text, unique=True, nullable=False)
    phone = db.Column(db.Text, unique=True, nullable=False)   
    address = db.Column(db.Text, nullable=False)
    post_code = db.Column(db.Text, nullable=False)
    city = db.Column(db.Text, nullable=False)
    country = db.Column(db.Text, nullable=False)

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    transaction_total = db.Column(db.Float, nullable=False)
    cart_value = db.Column(db.Float, nullable=False)
    postage_id = db.Column(db.Float, db.ForeignKey('postage.id'), nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    lastname = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text, nullable=False)    
    post_code = db.Column(db.Text, nullable=False)
    city = db.Column(db.Text, nullable=False)
    country = db.Column(db.Text, nullable=False)
    invoice = db.Column(db.Text, nullable=True)
    created = db.Column(db.DateTime, nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    payment_id = db.Column(db.Integer, db.ForeignKey('payment.id'), nullable=False)
    
class OrderProducts(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False )
    case_color_id = db.Column(db.Integer, db.ForeignKey('casecolors.id'), nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)
    content_color_id = db.Column(db.Integer, db.ForeignKey('contentcolors.id'), nullable=False)

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    product_name = db.Column(db.Text, nullable=False, unique=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    availability = db.Column(db.Integer, nullable=False)
    max_lines = db.Column(db.Integer, nullable=False)
    print_size = db.Column(db.Text)
    description = db.Column(db.Text)
    symbol = db.Column(db.Text)
    price = db.Column(db.Float)
    brand_cat = db.Column(db.Text)

class Brands(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand_name = db.Column(db.Text, nullable=False, unique=True)

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.Text, nullable=False, unique=True)

class Casecolors(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    case_color_name = db.Column(db.Text, nullable=False, unique=True)
    trodat = db.Column(db.Integer)
    wagraf = db.Column(db.Integer)
    colop = db.Column(db.Integer)

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line_1 = db.Column(db.Text, nullable=True)
    line_2 = db.Column(db.Text, nullable=True)
    line_3 = db.Column(db.Text, nullable=True)
    line_4 = db.Column(db.Text, nullable=True)
    line_5 = db.Column(db.Text, nullable=True)
    line_6 = db.Column(db.Text, nullable=True)
    line_7 = db.Column(db.Text, nullable=True)
    line_8 = db.Column(db.Text, nullable=True)
    line_9 = db.Column(db.Text, nullable=True)

class Contentcolors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content_color_name = db.Column(db.Text, nullable=False, unique=True)

class Postage(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    postage_name = db.Column(db.Text, nullable=False, unique=True)
    postage_price = db.Column(db.Float, nullable=False)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)
    content_color_id = db.Column(db.Integer, db.ForeignKey('contentcolors.id'), nullable=False)
    case_color_id = db.Column(db.Integer, db.ForeignKey('casecolors.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False) 

class Realization(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), primary_key=True, nullable=False)
    postage_info = db.Column(db.Text)
    paid = db.Column(db.Text, nullable=True)
    in_preparation = db.Column(db.Text, nullable=True)
    sent = db.Column(db.Text, nullable=True)
    returned = db.Column(db.Text, nullable=True)

class Invoices(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    company = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text, nullable=False)
    post_code = db.Column(db.Text, nullable=False)
    city = db.Column(db.Text, nullable=False)
    country = db.Column(db.Text, nullable=False)
    nip = db.Column(db.Text, nullable=False)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    payment_type = db.Column(db.Text, nullable=False)