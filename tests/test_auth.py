def test_login_page_loads(client):
    response = client.get("/auth/login")
    assert response.status_code == 200


def test_invalid_login(client):
    response = client.post(
        "/auth/login",
        data={
            "email": "wrong@test.com",
            "password": "wrongpass"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
