from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post,Category
from .forms import PostForm

# Create your views here.

def home(request):
    posts = Post.objects.order_by('-created_at')[:6]
    context = {
        'posts': posts,
    }
    return render(request, 'blog/home.html', context)

def blog_detail(request,id):
    categories = Category.objects.all()
    post = Post.objects.get(id=id)
    return render(request, 'blog/blog_detail.html', {'post':post, 'categories':categories})

@login_required
def write_blog(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blog/write_blog.html', {'form':form, 'categories':categories})         