from django.test import TestCase, Client
from django.urls import reverse


class TestBlogViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_post_list_view(self):
        url = reverse("blog:posts")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
