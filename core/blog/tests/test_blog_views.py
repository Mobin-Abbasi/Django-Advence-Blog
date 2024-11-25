from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime

from accounts.models import User, Profile
from ..models import Post


class TestBlogViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="test@test.com", password="test/@123456"
        )
        self.profile = Profile.objects.create(
            user=self.user,
            first_name="test first name",
            last_name="test last name",
            description="test description",
        )
        post = Post.objects.create(
            author=self.profile,
            title="test",
            content="discription",
            status=True,
            category=None,
            published_date=datetime.now(),
        )

    def test_post_list_view(self):
        url = reverse("blog:posts")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_post_detail_logged_in_response(self):
        self.client.force_login(self.user)
        url = reverse("blog:post-detail", kwargs={"pk": self.post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_detail_anonymous_response(self):
        url = reverse("blog:post-detail", kwargs={"pk": self.post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/blog/post/1/")
