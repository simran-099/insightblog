from django import forms
from .models import Comment, BlogPost

# 1️⃣ Comment Form
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'content']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Leave a comment...'}),
        }

# 2️⃣ BlogPost Form
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'author', 'category', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter blog title'}),
            'author': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write your blog content here...'}),
        }
