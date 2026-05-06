def test_login_wrong_password(client):
    client.post("/register", params={"name": "user3", "password": "1234"})

    response = client.post("/login", params={
        "name": "user3",
        "password": "wrong"
    })

    assert response.status_code == 401


def test_access_without_token(client):
    response = client.get("/get_tasks", params={"token": "invalid"})

    assert response.status_code == 401
