from rest_framework.test import APIClient
from django.urls import reverse
import pytest
from datetime import datetime

from accounts.models import User


@pytest.fixture
def common_user():
    user = User.objects.create_user(email="test@test.com", password="a/@123456")
    return user


@pytest.mark.django_db
class TestPostApi:
    """
    Test the API endpoints for Post model
    """

    client = APIClient()

    def test_get_post_response_200_status(self):
        """
        Test GET request to post list and check status code
        """
        url = reverse("blog:api-v1:post-list")
        response = self.client.get(url)
        assert response.status_code == 200

    def test_create_post_response_401_status(self):
        """
        Test creating a post response with a 401 status code
        """
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "test",
            "content": "description",
            "status": True,
            "published": datetime.now(),
        }
        response = self.client.post(url, data)
        assert response.status_code == 401

    def test_create_post_response_201_status(self, common_user):
        """
        Test creating a post response with a 201 status code
        """
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "test",
            "content": "description",
            "status": True,
            "published_date": datetime.now(),
        }
        user = common_user
        self.client.force_authenticate(user=user)
        response = self.client.post(url, data)
        assert response.status_code == 201

    def test_create_post_with_invalid_data_response_400_status(self, common_user):
        """
        Test creating a post with invalid data response with a 400 status code
        """
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "test",
            "content": "description",
        }
        user = common_user
        self.client.force_authenticate(user=user)
        response = self.client.post(url, data)
        assert response.status_code == 400
