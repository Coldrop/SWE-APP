# models/product_catalogue.py
from models.product import Product

class ProductCatalogue:
    _instance = None
    
    @classmethod
    def get_instance(cls, storage=None):
        if cls._instance is None:
            cls._instance = cls(storage)
        return cls._instance
    
    def __init__(self, storage):
        if self._instance is not None:
            raise Exception('Singleton instance already created')
        self.storage = storage
        self.products = {p['product_id']: Product(**p) for p in storage.load_products()} if storage else {}
    
    def add_product(self, product):
        self.products[product.product_id] = product
        if self.storage:
            self.storage.save_products(self.products.values())
    
    def update_product(self, product_id, name, description, price, stock, image):
        if product_id in self.products:
            product = self.products[product_id]
            product.name = name
            product.description = description
            product.price = price
            product.stock = stock
            product.image = image
            if self.storage:
                self.storage.save_products(self.products.values())
    
    def remove_product(self, product_id):
        if product_id in self.products:
            del self.products[product_id]
            if self.storage:
                self.storage.save_products(self.products.values())
    
    def archive_product(self, product_id):
        if product_id in self.products:
            self.products[product_id].archived = True
            if self.storage:
                self.storage.save_products(self.products.values())
    
    def get_all_products(self):
        return [p for p in self.products.values() if not p.archived]
    
    def get_product(self, product_id):
        return self.products.get(product_id)