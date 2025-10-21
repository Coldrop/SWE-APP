AWE Electronics Online Store

This is an e-commerce web app for Assignment 3 of SWE30003 – Software Architectures and Design . Built with Python 3.14 and Flask, it lets customers browse products, add to cart, order, and fake-pay, while admins manage stock. It uses MVC and saves data in JSON files, handling 150 users and keeping records for 7 years.


-Browse products (e.g., laptops) with prices/stock.
-Add/change/remove cart items, see total.
-Enter name/email/address to order.
-Mock payment with invoice.
-Admin panel to add/update/delete products.


Prerequisites
-Python 3.14 installed
-macOS or Windows
-Terminal

Setup
-Download the project folder.
-Open terminal, go to folder:
cd SWE-APP

-Install Flask:
pip install flask

-Run:
python app.py

-Open http://localhost:5000 in browser.


Folder Structure
awe-electronics-store/
├── app.py          # Main app
├── models/         # Code logic (e.g., shopping_cart.py)
├── routes/         # Page routes (e.g., store_routes.py)
├── templates/      # Web pages (e.g., home.html)
├── static/css/     # Styles (styles.css)
├── data/           # JSON data (e.g., products.json)


