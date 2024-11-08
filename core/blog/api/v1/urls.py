from django.urls import path
from . import views


app_name = "api-v1"


urlpatterns = [
    path('post/', views.post_list, name='post-list'),
]