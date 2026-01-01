def test_documents_requires_login(client):
    response = client.get("/documents/")
    assert response.status_code in (302, 401)
