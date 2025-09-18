from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post
from .forms import PostForm
from django.http import HttpResponseRedirect
from django.urls import reverse

def index(request):
    from django.core.paginator import Paginator
    post_list = Post.objects.all().order_by('-created_at')
    paginator = Paginator(post_list, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home/index.html', {'page_obj': page_obj})

@login_required
def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'home/add_post.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                next_page = request.GET.get('next', 'index')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please fill in all fields.')
    
    return render(request, 'home/login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if not all([username, email, password, confirm_password]):
            messages.error(request, 'Please fill in all fields.')
            return render(request, 'home/signup.html')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'home/signup.html')
        
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'home/signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'home/signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'home/signup.html')
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
        except Exception as e:
            messages.error(request, 'Error creating account. Please try again.')
    
    return render(request, 'home/signup.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('index')

@login_required
def profile_view(request):
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'home/profile.html', {
        'user': request.user,
        'user_posts': user_posts
    })

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        post.delete()
        messages.success(request, 'Post deleted successfully!')
    else:
        messages.error(request, "You don't have permission to delete this post.")
    
    return redirect('index')

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user.is_authenticated:
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            messages.success(request, 'Post unliked.')
        else:
            post.likes.add(request.user)
            messages.success(request, 'Post liked!')
    else:
        messages.error(request, 'You must be logged in to like posts.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'home/post_detail.html', {'post': post})