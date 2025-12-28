from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Count, Q
from django.utils.text import Truncator
from django.core.paginator import Paginator

from .models import Post, Comment, PostImage, Follow
from .forms import PostForm, CommentForm, SignUpForm, ProfileForm, UserUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login


def index(request):
    """
    Display all posts with pagination.
    Each post shows a truncated preview if content is long.
    """
    query = request.GET.get('q')
    if query:
        post_list = Post.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query)
        ).annotate(comment_count=Count('comments')).order_by('-created_at')
    else:
        post_list = Post.objects.annotate(comment_count=Count('comments')).order_by('-created_at')


    paginator = Paginator(post_list, 20)  # 50 posts per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "home/index.html", {"page_obj": page_obj})


@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

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
    User login view using Django's AuthenticationForm.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect(request.GET.get('next', 'index'))
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'home/login.html', {'form': form})


def signup_view(request):
    """
    User signup view using Custom SignUpForm.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = SignUpForm()

    return render(request, 'home/signup.html', {'form': form})


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
    Show profile page with user's posts and allow profile editing.
    """
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        # Ensure profile exists, though signal should handle it
        if not hasattr(request.user, 'profile'):
            from .models import Profile
            Profile.objects.create(user=request.user)
            
        p_form = ProfileForm(instance=request.user.profile)

    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    
    return render(request, 'home/profile.html', {
        'profile_user': request.user,
        'u_form': u_form,
        'p_form': p_form,
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
    liked = False
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        # messages.success(request, 'Post unliked.')
    else:
        post.likes.add(request.user)
        liked = True
        # messages.success(request, 'Post liked!')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'total_likes': post.total_likes()})

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def post_detail(request, pk):
    """
    Show post details with comments and gallery images.
    Allows adding a comment.
    """
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    images = post.images.all() 

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


def public_profile(request, username):
    """
    Show a public profile for any user.
    """
    profile_user = get_object_or_404(User, username=username)
    user_posts = Post.objects.filter(author=profile_user).order_by('-created_at')
    
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()
    
    return render(request, 'home/profile.html', {
        'profile_user': profile_user,
        'user_posts': user_posts,
        'is_following': is_following,
    })


@login_required
def follow_user(request, username):
    """
    Toggle follow status for a user.
    """
    user_to_follow = get_object_or_404(User, username=username)
    
    if user_to_follow != request.user:
        follow, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
        if not created:
            follow.delete()
            messages.success(request, f"Unfollowed {user_to_follow.username}.")
        else:
            messages.success(request, f"You are now following {user_to_follow.username}!")
            
    return redirect('public_profile', username=username)
