from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import PasswordChangeForm
from .models import Blog
from .forms import Edit_Blog
import ssl
import certifi

ssl._create_default_https_context = ssl.create_default_context(cafile=certifi.where())

def index(request):
    blog = Blog.objects.all()
    context = {'blogs': blog}
    return render(request, 'home.html', context)

from django.views.decorators.csrf import csrf_protect

def user_register(request):
    if request.method == 'POST':
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass')
        pass2 = request.POST.get('repass')

        if pass1 != pass2:
            messages.warning(request, 'Passwords do not match')
            return redirect('register')
        elif User.objects.filter(username=uname).exists():
            messages.warning(request, 'Username already taken')
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.warning(request, 'Email already taken')
            return redirect('register')
        else:
            user = User.objects.create_user(first_name=fname, last_name=lname, username=uname, email=email, password=pass1)
            user.save()
            subject = 'About Registration'
            message = f'Hi {uname}, You have been registered successfully on Kankavli college Blogs.'
            email_from = 'your-email@example.com'
            rec_list = [email]
            send_mail(subject, message, email_from, rec_list)
            messages.success(request, 'User has been registered successfully')
            return redirect('login')
    return render(request, 'register.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.warning(request, 'Invalid credentials')
            return redirect('login')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('/')

def post_blog(request):
    if request.method == "POST":
        title = request.POST.get('title')
        desc = request.POST.get('Description')
        img = request.FILES['image']
        blog = Blog(title=title, dsc=desc, user_id=request.user, Img=img)
        blog.save()
        messages.success(request, 'Post has been submitted successfully')
        return redirect('post_blog')
    return render(request, 'blog_post.html')

def blog_detail(request, id):
    blog = Blog.objects.get(id=id)
    context = {'blog': blog}
    return render(request, 'blog_detail.html', context)

def delete(request, id):
    blog = Blog.objects.get(id=id)
    blog.delete()
    messages.success(request, 'Post has been deleted')
    return redirect('/')

def edit(request, id):
    blog = Blog.objects.get(id=id)
    editblog = Edit_Blog(instance=blog)
    if request.method == 'POST':
        form = Edit_Blog(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post has been updated')
            return redirect('/')
    return render(request, 'edit_blog.html', {'edit_blog': editblog})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been changed')
            return redirect('/')
        else:
            messages.warning(request, 'Error')
            return redirect('change_password')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'PasswordChangeForm': form})



   
