from locust import HttpUser, task

class UserFlow(HttpUser):
    host = "http://127.0.0.1:8000"
    @task
    def full_flow(self):
        self.client.post("/register", params={
            "name": "user",
            "password": "1234"
        })

        login = self.client.post("/login", params={
            "name": "user",
            "password": "1234"
        }).json()

        token = login["token"]

        self.client.post("/add_tasks", params={
            "title": "task1",
            "token": token
        })

        self.client.get("/get_tasks", params={
            "token": token
        })
