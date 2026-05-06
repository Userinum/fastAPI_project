from auth import hash_password, verify_password, create_token


def test_password_hashing():
    password = "1234"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)


def test_create_token():
    token = create_token({"id": 1})
    assert isinstance(token, str)


def test_register_and_login(client):
    response = client.post("/register", params={
        "name": "user1",
        "password": "1234"
    })
    assert response.status_code == 200

    response = client.post("/login", params={
        "name": "user1",
        "password": "1234"
    })

    assert response.status_code == 200
    assert "token" in response.json()
