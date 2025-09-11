from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm

def index(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'home/index.html', {'posts': posts})

def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # go back to homepage
    else:
        form = PostForm()
    return render(request, 'home/add_post.html', {'form': form})
