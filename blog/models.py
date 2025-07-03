from django.db import models
from django.utils import timezone
from django.utils.html import strip_tags
import math

# ✅ Category model
class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

# ✅ BlogPost model
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    views = models.IntegerField(default=0)  # ✅ Added field for analytics

    def __str__(self):
        return self.title

    @property
    def read_time(self):
        plain_text = strip_tags(self.content)
        word_count = len(plain_text.split())
        return f"{math.ceil(word_count / 80)} min read"

# ✅ Comment model
class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.name}"

# ✅ Like model
class Like(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='likes')
    liked_by = models.CharField(max_length=100)
    liked_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Liked by {self.liked_by}"
