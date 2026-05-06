from locust import HttpUser, task, between
import uuid
class ApiUser(HttpUser):
    host = "http://127.0.0.1:8000"
    def on_start(self):
        self.username = f"user_{uuid.uuid4().hex[:8]}"
        self.password = "1234"
        self.token = None

        reg_response = self.client.post("/register", params={
            "name": self.username,
            "password": self.password
        })

        if reg_response.status_code != 200:
            return
        login_response = self.client.post("/login", params={
            "name": self.username,
            "password": self.password
        })

        if login_response.status_code == 200:
            try:
                self.token = login_response.json().get("token")
            except Exception:
                self.token = None

    @task(3)
    def create_task(self):
        if not self.token:
            return
        self.client.post("/add_tasks", params={
            "title": "task_from_locust",
            "token": self.token
        })

    @task(2)
    def get_tasks(self):
        if not self.token:
            return
        self.client.get("/get_tasks", params={
            "token": self.token
        })

    @task(1)
    def search_tasks(self):
        if not self.token:
            return
        self.client.get("/search", params={
            "query": "task",
            "token": self.token
        })

    @task(1)
    def top_tasks(self):
        if not self.token:
            return
        self.client.get("/top", params={
            "limit": 5,
            "token": self.token
        })
