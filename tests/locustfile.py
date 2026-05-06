from locust import HttpUser, task

class MyUser(HttpUser):

    @task
    def test_root(self):
        self.client.get("/")

    @task
    def test_register(self):
        self.client.post("/register", params={
            "name": "loaduser",
            "password": "1234"
        })
