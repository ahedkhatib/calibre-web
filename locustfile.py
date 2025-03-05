from locust import HttpUser, task, between

class CalibreUser(HttpUser):
    wait_time = between(1, 3)  # Simulate human-like delays
    #host = "http://localhost:8083"
    host = "https://f48f-2a06-c701-9fc9-5f00-83c-2461-70ac-e2c6.ngrok-free.app"

    @task
    def view_book_details(self):
        self.client.get("/book/6")

    @task
    def view_download(self):
        self.client.get("/download/stored/")
