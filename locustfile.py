from locust import HttpUser, between, task

class NotesUser(HttpUser):
    wait_time = between(0.5, 1.5)   # пауза между действиями пользователя

    @task(3)
    def list_notes(self):
        self.client.get("/")

    @task(1)
    def filter_category(self):
        self.client.get("/?category=7&active=1", name="/?category")

    @task(1)
    def search(self):
        self.client.get("/?q=дело", name="/?q")