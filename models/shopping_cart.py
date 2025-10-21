# models/shopping_cart.py
from models.cart_item import CartItem

class ShoppingCart:
    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.items = {}
    
    def add_item(self, product, quantity):
        if product.reduce_stock(quantity):
            if product.product_id in self.items:
                self.items[product.product_id].quantity += quantity
            else:
                self.items[product.product_id] = CartItem(product, quantity)
        else:
            raise ValueError('Insufficient stock')
    
    def remove_item(self, product_id):
        if product_id in self.items:
            del self.items[product_id]
    
    def update_quantity(self, product_id, quantity):
        if product_id in self.items:
            if quantity <= 0:
                self.remove_item(product_id)
            else:
                current_qty = self.items[product_id].quantity
                product = self.items[product_id].product
                if product.reduce_stock(quantity - current_qty):
                    self.items[product_id].quantity = quantity
                else:
                    raise ValueError('Insufficient stock')
    
    def calculate_total(self):
        return sum(item.get_total_price() for item in self.items.values())
    
    def get_items(self):
        return list(self.items.values())
    
    def clear_cart(self):
        self.items.clear()
