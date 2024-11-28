from locust import HttpUser, task, between


class QuickstartUser(HttpUser):

    def on_start(self):
        response = self.client.post(
            "/accounts/api/v1/jwt/create/",
            {"email": "admin@admin.com", "password": "Mm123456789"},
        ).json()
        self.client.headers = {"Authorization": f"Bearer {response.get('access')}"}

    @task
    def post_list(self):
        self.client.get("/blog/api/v1/post/")

    @task
    def category_list(self):
        self.client.get("/blog/api/v1/category/")