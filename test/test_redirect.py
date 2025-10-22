def test_logout_redirect(client):
    response = client.get("/", follow_redirects=True)
    assert len(response.history) == 2
    assert response.request.path == "/store/"
