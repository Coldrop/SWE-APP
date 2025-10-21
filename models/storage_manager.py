# models/storage_manager.py
import json
import os
from models.product import Product
from models.shopping_cart import ShoppingCart
from models.customer import Customer
from models.cart_item import CartItem

class StorageManager:
    def __init__(self):
        self.data_dir = 'data'
        os.makedirs(self.data_dir, exist_ok=True)
        self.files = {
            'products': f'{self.data_dir}/products.json',
            'customers': f'{self.data_dir}/customers.json',
            'carts': f'{self.data_dir}/carts.json',
            'orders': f'{self.data_dir}/orders.json',
            'invoices': f'{self.data_dir}/invoices.json'
        }
    
    def load_products(self):
        return self._load_json(self.files['products'], [
            {'product_id': 1, 'name': 'Laptop', 'description': 'Powerful i7 laptop', 'price': 1500, 'stock': 10, 'image': 'laptop.jpg', 'archived': False},
            {'product_id': 2, 'name': 'Smartphone', 'description': 'Latest model with OLED display', 'price': 999, 'stock': 15, 'image': 'phone.jpg', 'archived': False},
            {'product_id': 3, 'name': 'Headphones', 'description': 'Noise cancelling', 'price': 299, 'stock': 25, 'image': '', 'archived': False}
        ])
    
    def save_products(self, products):
        self._save_json(self.files['products'], [p.__dict__ for p in products])
    
    def load_customer(self, customer_id):
        customers = self._load_json(self.files['customers'], [])
        for c in customers:
            if c['id'] == customer_id:
                return Customer(**c)
        return None
    
    def save_customer(self, customer):
        customers = self._load_json(self.files['customers'], [])
        customers = [c for c in customers if c['id'] != customer.id]
        customer_dict = {'id': customer.id, 'name': customer.name, 'email': customer.email, 'address': customer.address}
        customers.append(customer_dict)
        self._save_json(self.files['customers'], customers)
    
    def load_cart(self, customer_id):
        carts = self._load_json(self.files['carts'], [])
        for c in carts:
            if c['customer_id'] == customer_id:
                cart = ShoppingCart(customer_id)
                cart.items = {item['product']['product_id']: CartItem(Product(**item['product']), item['quantity']) for item in c['items']}
                return cart
        return None
    
    def save_cart(self, cart):
        carts = self._load_json(self.files['carts'], [])
        carts = [c for c in carts if c['customer_id'] != cart.customer_id]
        carts.append({
            'customer_id': cart.customer_id,
            'items': [{'product': item.product.__dict__, 'quantity': item.quantity} for item in cart.get_items()]
        })
        self._save_json(self.files['carts'], carts)
    
    def load_orders(self):
        return self._load_json(self.files['orders'], [])
    
    def save_order(self, order):
        orders = self._load_json(self.files['orders'], [])
        orders.append({
            'id': order.id,
            'customer_id': order.customer_id,
            'items': [{'product': item.product.__dict__, 'quantity': item.quantity, 'subtotal': item.subtotal} for item in order.items],
            'total': order.total,
            'delivery_address': order.delivery_address,
            'status': order.status
        })
        self._save_json(self.files['orders'], orders)
    
    def load_invoices(self):
        return self._load_json(self.files['invoices'], [])
    
    def save_invoice(self, invoice):
        invoices = self._load_json(self.files['invoices'], [])
        invoices = [i for i in invoices if i['invoice_id'] != invoice.invoice_id]
        invoices.append(invoice.__dict__)
        self._save_json(self.files['invoices'], invoices)
    
    def _load_json(self, file_path, default):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return default
    
    def _save_json(self, file_path, data):
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
