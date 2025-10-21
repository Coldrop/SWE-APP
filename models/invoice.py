# models/invoice.py
class Invoice:
    def __init__(self, order_id, total):
        self.order_id = order_id
        self.invoice_id = f'I{order_id}'
        self.total = total
        self.status = 'Unpaid'
    
    def pay(self):
        self.status = 'Paid'