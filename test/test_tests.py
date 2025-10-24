def test_store_redirect(client):
    response = client.get("/", follow_redirects=True)
    assert len(response.history) == 2
    assert response.request.path == "/store/"

def test_add_to_cart(client):
    response = client.post("/store/cart/add/1", data = { "quantity": 1 }, follow_redirects=True)
    assert response.request.path == "/store/cart"
    assert b'<form method="POST" action="/store/cart/update/1">' in response.data

def test_order(client):
    client.post("/store/cart/add/1", data = { "quantity": 1 })
    response = client.post("/store/order/confirm", data = { "name": "test", "email": "test@test.test", "address": "192.168 Test Avenue" }, follow_redirects=True)
    assert response.request.path == "/store/order/payment"
    assert b'<li class="success">Order placed!</li>' in response.data
    response = client.post("/store/order/payment", data = { "payment_method": "PayPal" }, follow_redirects=True)
    assert response.request.path == "/store/"
    assert b'<li class="success">Payment successful!</li>' in response.data
