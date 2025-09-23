from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Count
from django.utils.text import Truncator
from django.core.paginator import Paginator

from .models import Post, Comment, PostImage
from .forms import PostForm, CommentForm
from django.http import HttpResponse

def health_check(request):
    return HttpResponse("OK")



def index(request):
    """
    Display all posts with pagination.
    Each post shows a truncated preview if content is long.
    """
    post_list = Post.objects.annotate(comment_count=Count('comments')).order_by('-created_at')

    for post in post_list:
        truncated = Truncator(post.content).words(3000, truncate=' ...')
        post.preview_content = truncated
        post.show_read_more = truncated != post.content

    paginator = Paginator(post_list, 50)  # 50 posts per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "home/index.html", {"page_obj": page_obj})


@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # Save main post (with optional cover image)
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            # Handle multiple images
            gallery_images = request.FILES.getlist('images')
            for img in gallery_images:
                PostImage.objects.create(post=post, image=img)

            messages.success(request, "Post added successfully!")
            return redirect('index')
        else:
            messages.error(request, "There was an error with your submission.")
    else:
        form = PostForm()

    return render(request, 'home/add_post.html', {'form': form})



def login_view(request):
    """
    User login view.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect(request.GET.get('next', 'index'))
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please fill in all fields.')

    return render(request, 'home/login.html')


def signup_view(request):
    """
    User signup view with basic validation.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Basic validations
        if not all([username, email, password, confirm_password]):
            messages.error(request, 'Please fill in all fields.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
        else:
            # Create user
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')

    return render(request, 'home/signup.html')


def logout_view(request):
    """
    Logout the user and redirect to home.
    """
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('index')


@login_required
def profile_view(request):
    """
    Show profile page with user's posts.
    """
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'home/profile.html', {
        'user': request.user,
        'user_posts': user_posts
    })


@login_required
def delete_post(request, pk):
    """
    Delete a post if the current user is the author.
    """
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        post.delete()
        messages.success(request, 'Post deleted successfully!')
    else:
        messages.error(request, "You don't have permission to delete this post.")

    return redirect('index')


@login_required
def like_post(request, pk):
    """
    Toggle like/unlike for a post.
    """
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        messages.success(request, 'Post unliked.')
    else:
        post.likes.add(request.user)
        messages.success(request, 'Post liked!')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def post_detail(request, pk):
    """
    Show post details with comments and gallery images.
    Allows adding a comment.
    """
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    images = post.images.all()  # all gallery images

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()

    return render(request, 'home/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'images': images
    })


@login_required
def add_comment(request, pk):
    """
    Add a comment to a post.
    """
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Invalid comment submission.')

    return redirect('post_detail', pk=post.pk)


@login_required
def delete_comment(request, pk):
    """
    Delete a comment if the user is either the comment author or post author.
    """
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post

    if request.user == comment.author or request.user == post.author:
        comment.delete()
        messages.success(request, 'Comment deleted successfully!')
    else:
        messages.error(request, "You don't have permission to delete this comment.")

    return redirect('post_detail', pk=post.pk)
