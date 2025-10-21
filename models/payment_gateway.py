# models/payment_gateway.py
class IPaymentGateway:
    def process_payment(self, invoice):
        raise NotImplementedError('Must implement in subclass')

class MockPaymentGateway(IPaymentGateway):
    def process_payment(self, invoice):
        print(f'Simulating payment for invoice: {invoice.invoice_id}')
        invoice.pay()
        return True