from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.product_catalogue import ProductCatalogue
from models.product import Product
from models.storage_manager import StorageManager

admin_blueprint = Blueprint('admin', __name__)
storage = StorageManager()
catalogue = ProductCatalogue.get_instance(storage)

@admin_blueprint.route('/')
def admin_home():
    products = catalogue.get_all_products()
    return render_template('admin.html', products=products)

@admin_blueprint.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_id = len(catalogue.get_all_products()) + 1
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        image = request.form.get('image', '')
        product = Product(product_id, name, description, price, stock, image)
        catalogue.add_product(product)
        flash('Product added!', 'success')
        return redirect(url_for('admin.admin_home'))
    return render_template('add_product.html')

@admin_blueprint.route('/update/<int:product_id>', methods=['GET', 'POST'])
def update_product(product_id):
    product = catalogue.get_product(product_id)
    if not product:
        flash('Product not found!', 'error')
        return redirect(url_for('admin.admin_home'))
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        image = request.form.get('image', '')
        catalogue.update_product(product_id, name, description, price, stock, image)
        flash('Product updated!', 'success')
        return redirect(url_for('admin.admin_home'))
    return render_template('update_product.html', product=product)

@admin_blueprint.route('/delete/<int:product_id>')
def delete_product(product_id):
    catalogue.remove_product(product_id)
    flash('Product deleted!', 'success')
    return redirect(url_for('admin.admin_home'))

@admin_blueprint.route('/archive/<int:product_id>')
def archive_product(product_id):
    catalogue.archive_product(product_id)
    flash('Product archived!', 'success')
    return redirect(url_for('admin.admin_home'))