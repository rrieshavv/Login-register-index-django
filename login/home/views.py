from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse
from django.contrib import messages


# Create your views here.


def index(request):
    if request.user.is_anonymous:
        return redirect('/login')
    return render(request, 'index.html')

def loginUser(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        # check if user has entered correct credential
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            messages.warning(request, 'Account credentials does not exist')
            return render(request, 'login.html')


    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect('/login')

def registerUser(request):
    if request.method=='POST':
        # Get the post parameter
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # checks for error
        if len(username) > 15:
            messages.warning(request, "Username must be under 15 characters")
            return redirect('/register')
        
        if not username.isalnum():
            messages.warning(request, 'Username can only contain letters and numbers.')
            return redirect('/register')

        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Username already exists.')
            return redirect('/register')

        if len(password1) <= 8:
            messages.warning(request, 'Passwords should contain atleast 8 characters.')
            return redirect('/register')

        if password1 != password2:
            messages.warning(request, "Passwords do not match")
            return redirect('/register')
        



        # Create user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, 'Your account was created!')
        return redirect('/login')

    return render(request, 'register.html')

