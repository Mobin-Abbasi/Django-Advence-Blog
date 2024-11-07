from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Post, Category


def index_view(request):
    return render(request, 'index.html')