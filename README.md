# <img src="app/static/stampicon.png" alt="stamp_icon" width="35"/> **MG Print | online store**

## Video demo: https://youtu.be/s67WPO_GYU4

An online store with Flask server-side, Flask-SQLAlchemy ORM for Sqlite database, and Javascript front-end combining Bootstrap framework and personalised CSS.  

Functionalities include:
- Dynamically rendered single-product pages and multi-product category pages.
- User registration and login.
- Dynamically rendered order page whose template adjusts to user's status (logged in vs. registered but not logged in vs. not registered).
- Dynamically rendered cart modal with a function for deleting a product from the cart.
- Cart products stored in localStorage. Information on ordered products sent to server only once the user finalized an order.

## **Files description**
1. **run.py** - a runner file that starts the app

2. **__init__.py** - a script with app configuration, database connection configuration.

3. **views** - folder stores scripts for all routes:
- **views_register.py** - a script for registration page.
- **views_login.py** - a script for a login page. The script connects to a database
to check if the username and password that the user enters exist and that password
corresponds with the username. 
- **views_password.py** - this script allows a user who is registered and loged in to 
change their password. The script chacks if the new password entered by the user
fullfills the requirements and connects to database to change the saved password.
- **views_product.py** - this script creates a dynamically renderd pages for each
product in the database. The script connects to a database to fetch information
about a product and fills this information(i.e. product name, price, number of lines
of text that this product allows on a rubber stamp plate) in the **product.html** template.
- **views_brand_all.py** - this a script for dynamically rendered page that shows
in a category chosen by the user(for example when user is redirected to page that shows
all products of the same brand and products of the same type). The script connect
to a database to collect data for all products that belong to a given category.
- **views_order.py**  - this is a script for **order.html** template where a user
can finalize their order. This script dynamically displays **order.html**. If a user 
is already logged in the order form will display user datails collected from the database.
If user is not logged in the full order form will be displayed that askes the user
to enter all details necessery to complete the order. The user can make an order
without registering but they can also fill in a password field to get register 
on the server. This scrip also collects order details entered by the user and saves
this information in the database.
- **views.py** - this files contains a few smaller routes, including a dinamically
rendered landing page.

4. **helpers.py** - this scrip contains a few helpers functions used by routes scripts.

5. **models.py** - script that creates all Flask-SQLAlchemy models for the database.

6. **templates** folder - contains different html templates used by the routes.

7. **store.js** in **static** folder - Javascript code that manages front-end functionalities.
It contains function for:
- dynamically rendering **product.html** template when user enters product customisation
details the displayed price changes depending on the number of lines of text that
a user would like to order on the rubber stamp.
- adding products to cart when a user customises a product on the **product.html**
page and hits and "add-to-cart button". Information about a product that
user adds to cart and customization details are sent the user browser's local storage,
where they are stored until the user finanlizes an order on **order.html** page.
- fetching information from the browser's local storage to display it in the cart modal,
which displays to the user all products in the user's cart.
- fetching information from the browser's local storage and preparing it to be 
sent to the server when a user finalizes an order on the **order.html** page.
- an **add-to-cart modal** - a modal that is displayed when a user adds a product to cart.
- a **cart modal** - a modal that is displayed when a user clicks on the **cart icon** to see what
is already in their cart. The **cart modal** has a feature for deleting a product from 
the cart. This function deletes a product from the browser's local storage and
and updates displayed products in the cart modal.

8. **styles.css** file in the **static** folder - contains personalised ccs code.
















NB. Store still under constraction.