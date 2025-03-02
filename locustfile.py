from locust import HttpUser, task, between

class CalibreUser(HttpUser):
    wait_time = between(1, 3)  # Simulate human-like delays
    host = "https://5d61-2a06-c701-7128-9b00-9800-a72e-7239-d87.ngrok-free.app"

    @task
    def view_book_details(self):
        self.client.get("/book/6")

    @task
    def view_download(self):
        self.client.get("/download/stored/")
