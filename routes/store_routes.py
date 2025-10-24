from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from models.product_catalogue import ProductCatalogue
from models.customer import Customer
from models.order import Order
from models.invoice import Invoice
from models.payment_gateway import MockPaymentGateway
from models.storage_manager import StorageManager

store_blueprint = Blueprint('store', __name__)
storage = StorageManager()
catalogue = ProductCatalogue.get_instance(storage)

def get_customer():
    if 'user_id' not in session:
        session['user_id'] = 'C001'
        customer = Customer('C001', 'Guest', 'guest@example.com')
        storage.save_customer(customer)
    return storage.load_customer(session['user_id'])

@store_blueprint.route('/')
def home():
    products = catalogue.get_all_products()
    return render_template('home.html', products=products)

@store_blueprint.route('/product/<int:product_id>')
def view_product(product_id):
    product = catalogue.get_product(product_id)
    if not product or product.archived:
        flash('Product not found!', 'error')
        return redirect(url_for('store.home'))
    return render_template('product.html', product=product)

@store_blueprint.route('/cart')
def view_cart():
    customer = get_customer()
    return render_template('cart.html', cart=customer.get_cart(storage))

@store_blueprint.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    customer = get_customer()
    product = catalogue.get_product(product_id)
    if not product or product.archived:
        flash('Product not found!', 'error')
        return redirect(url_for('store.view_product', product_id=product_id))
    quantity = int(request.form['quantity'])
    cart = customer.get_cart(storage)
    cart.add_item(product, quantity)
    storage.save_cart(cart)
    flash('Item added!', 'success')
    return redirect(url_for('store.view_cart'))

@store_blueprint.route('/cart/update/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    customer = get_customer()
    quantity = int(request.form['quantity'])
    cart = customer.get_cart(storage)
    cart.update_quantity(product_id, quantity)
    storage.save_cart(cart)
    flash('Cart updated!', 'success')
    return redirect(url_for('store.view_cart'))

@store_blueprint.route('/cart/remove/<int:product_id>')
def remove_from_cart(product_id):
    customer = get_customer()
    cart = customer.get_cart(storage)
    cart.remove_item(product_id)
    storage.save_cart(cart)
    flash('Item removed!', 'success')
    return redirect(url_for('store.view_cart'))

@store_blueprint.route('/order/confirm', methods=['GET', 'POST'])
def confirm_order():
    customer = get_customer()
    cart = customer.get_cart(storage)
    if not cart.get_items():
        flash('Cart is empty!', 'error')
        return redirect(url_for('store.view_cart'))
    if request.method == 'POST':
        customer.name = request.form['name']
        customer.email = request.form['email']
        customer.address = request.form['address']
        storage.save_customer(customer)
        order = Order(f'O{len(storage.load_orders()) + 1}', customer.id, cart.get_items(), customer.address)
        invoice = Invoice(order.id, order.total)
        storage.save_order(order)
        storage.save_invoice(invoice)
        cart.clear_cart()
        storage.save_cart(cart)
        session['invoice_id'] = invoice.invoice_id
        flash('Order placed!', 'success')
        return redirect(url_for('store.simulate_payment'))
    return render_template('confirm_order.html', cart=cart)

@store_blueprint.route('/order/payment', methods=['GET', 'POST'])
def simulate_payment():
    invoice_id = session.get('invoice_id')
    if not invoice_id:
        flash('No invoice found!', 'error')
        return redirect(url_for('store.home'))
    invoices = storage.load_invoices()
    invoice = next((i for i in invoices if i['invoice_id'] == invoice_id), None)
    if not invoice:
        flash('Invoice not found!', 'error')
        return redirect(url_for('store.home'))
    if request.method == 'POST':
        gateway = MockPaymentGateway()
        invoice_obj = Invoice(invoice['order_id'], invoice['total'])
        if gateway.process_payment(invoice_obj):
            invoice['status'] = 'Paid'
            storage.save_invoice(invoice_obj)
            orders = storage.load_orders()
            for o in orders:
                if o['id'] == invoice['order_id']:
                    o['status'] = 'Paid'
            storage._save_json(storage.files['orders'], orders)
            flash('Payment successful!', 'success')
            return redirect(url_for('store.home'))
        flash('Payment failed!', 'error')
    return render_template('payment.html', invoice=invoice)
