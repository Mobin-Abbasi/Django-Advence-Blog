from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=250)
    
    def __str__(self):
        return self.name


class Post(models.Model):
    """
    This is a class to define posts in a blog app.
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    title = models.CharField(max_length=250)
    content = models.TextField()
    status = models.BooleanField(default=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, related_name='subcategories', null=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField()
    
    class Meta:
        ordering = ['-created_date']
        indexes = [
            models.Index(fields=['-created_date'])
        ]

    def __Str__(self):
        return self.title