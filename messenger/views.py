from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Q

@login_required
def home_page(request):
    chats = Chat.objects.filter(
        
        Q(user1 = request.user) | Q(user1 = request.user)
    
    )
    
    return render(request, 'home.html', {"chats": chats})


@login_required
def logout_user(request):
    logout(request)
    return redirect("login")

def registration(request):

    if request.method == 'POST':
        data = request.POST
        if User.objects.filter(username = data['username'], password = data['password']).exists():
            return redirect("login")

        User.objects.create_user(
            username = data['username'],
            password = data['password'],
            avatar = request.FILES.get("avatar"),
            first_name = data['first_name']
        )

        return redirect("login")

    return render(request, "registration.html")






def login_user(request):

    if request.method == 'POST':
        data = request.POST
        user = authenticate(username = data['username'], password = data['password'])

        if user is None:
            return redirect("login")

        login(request, user)
        return redirect("home")

    return render(request, "login.html")



@login_required
def profile(request):
    return render(request, "profile.html")


@login_required
def get_users(request):
    users = User.objects.exclude(username = request.user.username)
    return render(request, "users.html", {"users": users})