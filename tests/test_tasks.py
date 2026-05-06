def create_user_and_token(client):
    client.post("/register", params={"name": "user2", "password": "1234"})
    response = client.post("/login", params={"name": "user2", "password": "1234"})
    return response.json()["token"]


def test_create_task(client):
    token = create_user_and_token(client)

    response = client.post("/add_tasks", params={
        "title": "task1",
        "token": token
    })

    assert response.status_code == 200
    assert response.json()["title"] == "task1"


def test_get_tasks(client):
    token = create_user_and_token(client)

    client.post("/add_tasks", params={"title": "task1", "token": token})
    client.post("/add_tasks", params={"title": "task2", "token": token})

    response = client.get("/get_tasks", params={"token": token})

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_delete_task(client):
    token = create_user_and_token(client)

    task = client.post("/add_tasks", params={
        "title": "task_delete",
        "token": token
    }).json()

    response = client.delete(f"/tasks/{task['id']}", params={"token": token})

    assert response.status_code == 200
    assert response.json()["Все прошло четко!"] == 1


def test_search_tasks(client):
    token = create_user_and_token(client)

    client.post("/add_tasks", params={"title": "python", "token": token})
    client.post("/add_tasks", params={"title": "java", "token": token})

    response = client.get("/search", params={
        "query": "python",
        "token": token
    })

    assert len(response.json()) == 1


def test_top_tasks(client):
    token = create_user_and_token(client)

    client.post("/add_tasks", params={"title": "low", "token": token})
    client.post("/add_tasks", params={"title": "high", "token": token})

    response = client.get("/top", params={
        "limit": 1,
        "token": token
    })

    assert len(response.json()) == 1
