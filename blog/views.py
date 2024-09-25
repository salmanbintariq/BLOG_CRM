from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import Post,Category,Comment
from .forms import PostForm, CommentForm


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

@login_required
def dashboard(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'blog/dashboard.html', {"posts":posts, "user":request.user, "post_count": posts.count()})

@login_required
def blog_detail(request,slug):
    categories = Category.objects.all()
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(parent=None) # Get only top-level comments

    # Comment form handling
    if request.method == 'POST':
        parent_id = request.POST.get('parent_id')
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            if parent_id:
                comment.parent_id = parent_id
            comment.save()
            return redirect('blog-detail', slug=post.slug)
    else:
        comment_form = CommentForm()

    context = {
        'post':post,
        'categories':categories,
        'comments':comments,
        'comment_form':comment_form
    }        

    return render(request, 'blog/blog_detail.html', context)

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

@login_required
def edit_blog(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('dashboard')
    else:
        form = PostForm(instance=post)    
    return render(request, 'blog/edit.html', {'form': form, 'post': post})    
@login_required
def delete_blog(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('dashboard')
    
@login_required    
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Comment updated!")
            return redirect('blog-detail', slug=comment.post.slug)
        else:
            messages.error(request, "Failed to update comment. Please check your input.")
    
    return redirect('blog-detail', slug=comment.post.slug)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        comment.delete()
        messages.success(request, "Comment deleted!")
        
    return redirect('blog-detail', slug=comment.post.slug)