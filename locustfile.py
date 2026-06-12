from locust import HttpUser, task, between

class ProjectPerformanceUser(HttpUser):
    wait_time = between(1, 3)
    @task(3)
    def view_catalog(self):
        self.client.get("/entries")

    @task(1)
    def view_phone_category(self):
        payload = {"cat": "phone"}
        self.client.post("/bycat", json=payload)