from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Post,Category
from .forms import PostForm


# Create your views here.

def home(request):
    query = request.GET.get('q', '')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        ).order_by('-created_at')
    else:
        posts = Post.objects.order_by('-created_at')    

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

def category_blogs(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(categories=category)    
    return render(request, 'blog/category_blogs.html', {'category':category, "posts":posts})