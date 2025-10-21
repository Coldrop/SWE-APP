# models/product.py
class Product:
    def __init__(self, product_id, name, description, price, stock, image='', archived=False):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.image = image
        self.archived = archived
    
    def is_in_stock(self, quantity):
        return self.stock >= quantity
    
    def reduce_stock(self, quantity):
        if self.is_in_stock(quantity):
            self.stock -= quantity
            return True
        return False
