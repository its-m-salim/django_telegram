from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import User


@login_required
def home_page(request):
    return render(request, 'home.html')


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
            avatar = request.FILES.get("avatar")
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



