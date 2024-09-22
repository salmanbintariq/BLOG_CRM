from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.", extra_tags='error')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.", extra_tags='error')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.", extra_tags='error')
            return redirect('register')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Registration successful! You can now log in.", extra_tags='success')
        return redirect('register')
    
    return render(request, 'users/register.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to your desired page after login
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'users/login.html')

def logout_user(request):
    logout(request)
    return redirect('home')
