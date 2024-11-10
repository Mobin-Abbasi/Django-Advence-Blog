from django.shortcuts import render
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Category
from .forms import PostForm


class PostListView(ListView):
    model = Post
    template_name = "index.html"
    context_object_name = "posts"


class PostDetailView(DetailView):
    model = Post
    template_name = "detail.html"


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    success_url = "/blog/post/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_url = "/blog/post/"


class PostDeleteView(DeleteView):
    model = Post
    success_url = "/blog/post/"
