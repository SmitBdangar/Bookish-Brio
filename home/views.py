from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm

def index(request):
    from django.core.paginator import Paginator
    post_list = Post.objects.all().order_by('-created_at')
    paginator = Paginator(post_list, 50)  # 50 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home/index.html', {'page_obj': page_obj})

def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # go back to homepage
    else:
        form = PostForm()
    return render(request, 'home/add_post.html', {'form': form})
