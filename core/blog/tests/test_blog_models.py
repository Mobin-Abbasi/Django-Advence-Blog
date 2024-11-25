# from django.test import TestCase
# from datetime import datetime

# from ..models import Post, Category
# from accounts.models import User, Profile


# class TestPostModel(TestCase):
#     """This class implements the post model interface for the post model"""

#     def setUp(self):
#         self.user = User.objects.create_user(
#             email="test@test.com", password="test/@123456"
#         )
#         self.profile = Profile.objects.create(
#             user=self.user,
#             first_name="test first name",
#             last_name="test last name",
#             description="test description",
#         )

#     def test_create_post_with_valid_data(self):
#         post = Post.objects.create(
#             author=self.profile,
#             title="test",
#             content="discription",
#             status=True,
#             category=None,
#             published_date=datetime.now(),
#         )
#         self.assertTrue(Post.objects.filter(pk=post.id).exists())
