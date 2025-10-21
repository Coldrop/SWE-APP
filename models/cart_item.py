# models/cart_item.py
class CartItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity
    
    def get_total_price(self):
        return self.product.price * self.quantity