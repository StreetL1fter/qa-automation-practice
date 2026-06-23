from locust import HttpUser, task, between
import uuid
import logging

logger = logging.getLogger(__name__)


class ProjectPerformanceUser(HttpUser):
    wait_time = between(3, 7)
    def on_start(self):
        self.username = f"user_{uuid.uuid4().hex[:8]}"
        self.password = "secure_password123"
        payload = {
            "username": self.username,
            "password": self.password
        }
        response = self.client.post("/login", json=payload)
        if response.status_code == 200:
            logger.info(f"Пользователь {self.username} успешно авторизован под нагрузкой")
        else:
            logger.info(f"Ошибка пользователя {self.username}")
    @task(3)
    def view_catalog(self):
        self.client.get("/entries")

    @task(1)
    def view_phone_category(self):
        payload = {"cat": "phone"}
        self.client.post("/bycat", json=payload)
        