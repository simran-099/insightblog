from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.admin.views.decorators import staff_member_required

from .models import BlogPost, Comment, Like
from .forms import CommentForm, BlogPostForm


# ✅ Home Page with Search & Category Filter
def home(request):
    query = request.GET.get('q')
    selected_category = request.GET.get('category')

    posts = BlogPost.objects.all()

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(category__name__icontains=query)
        )

    if selected_category:
        posts = posts.filter(category__name=selected_category)

    posts = posts.order_by('-created_at')
    categories = BlogPost.objects.values_list('category__name', flat=True).distinct()

    return render(request, 'blog/home.html', {
        'posts': posts,
        'categories': categories,
        'selected_category': selected_category
    })


# ✅ Post Detail + Comment + View Count
def post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)

    post.views += 1
    post.save(update_fields=["views"])

    comments = Comment.objects.filter(post=post)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            form = CommentForm()
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })


# ✅ Create Blog Post
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BlogPostForm()
    return render(request, 'blog/create_post.html', {'form': form})


# ✅ Like Blog Post
def like_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        Like.objects.create(post=post, liked_by="Anonymous")
    return HttpResponseRedirect(reverse('post_detail', args=[pk]))


# ✅ Edit Blog Post
def edit_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})


# ✅ Delete Blog Post
def delete_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Blog post deleted successfully.')
        return redirect('home')
    return render(request, 'blog/delete_post.html', {'post': post})


# ✅ User Signup
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'blog/signup.html', {'form': form})


# ✅ Admin-only Analytics Dashboard
@staff_member_required
def analytics_dashboard(request):
    total_posts = BlogPost.objects.count()
    total_views = sum(post.views for post in BlogPost.objects.all())
    total_likes = Like.objects.count()
    total_comments = Comment.objects.count()

    return render(request, 'blog/analytics_dashboard.html', {
        'total_posts': total_posts,
        'total_views': total_views,
        'total_likes': total_likes,
        'total_comments': total_comments,
    })
