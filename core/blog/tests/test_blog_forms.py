from django.test import TestCase
from datetime import datetime

from ..forms import PostForm
from ..models import Category


class TestPostForm(TestCase):
    """This class implements the post form"""

    def test_post_form_with_valid_data(self):
        category_obj = Category.objects.create(name="hello")
        form = PostForm(
            data={
                "title": "title",
                "content": "description",
                "category": category_obj,
                "status": True,
                "published_date": datetime.now(),
            }
        )
        self.assertTrue(form.is_valid())

    def test_post_form_with_no_data(self):
        form = PostForm(data={})
        self.assertFalse(form.is_valid())
