# models/order.py
class OrderItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity
        self.subtotal = product.price * quantity

class Order:
    def __init__(self, id, customer_id, items, delivery_address):
        self.id = id
        self.customer_id = customer_id
        self.items = [OrderItem(item.product, item.quantity) for item in items]
        self.total = sum(item.subtotal for item in self.items)
        self.delivery_address = delivery_address
        self.status = 'Pending'
    
    def mark_as_paid(self):
        self.status = 'Paid'
