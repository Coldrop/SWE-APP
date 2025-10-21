# models/customer.py
from models.shopping_cart import ShoppingCart

class Customer:
    def __init__(self, id, name, email, address='', **kwargs):
        self.id = id
        self.name = name
        self.email = email
        self.address = address
        self.cart = None
    
    def get_cart(self, storage):
        if not self.cart:
            self.cart = storage.load_cart(self.id) or ShoppingCart(self.id)
        return self.cart
