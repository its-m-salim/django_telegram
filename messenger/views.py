import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Q

AVATAR_COLORS = ["#e17076", "#faa774", "#a695e7", "#7bc862", "#6ec9cb", "#65aadd", "#ee7aae"]


@login_required
def home_page(request):
    chats = Chat.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    ).order_by("-created_at")

    items = []
    for chat in chats:
        if chat.user1 == request.user:
            other = chat.user2
        else:
            other = chat.user1
        items.append({"chat": chat, "other": other})

    return render(request, "home.html", {"items": items})


@login_required
def logout_user(request):
    logout(request)
    return redirect("login")


def registration(request):

    if request.method == 'POST':
        data = request.POST
        color = data.get("avatar_color")

        if color not in AVATAR_COLORS:
            color = random.choice(AVATAR_COLORS)

        if User.objects.filter(username=data['username']).exists():
            return redirect("login")

        user = User.objects.create_user(
            username=data['username'],
            password=data['password'],
            first_name=data['first_name'],
            avatar=request.FILES.get("avatar"),
            avatar_color=color
        )

        login(request, user)
        return render(request, "registration_success.html")

    return render(request, "registration.html", {"avatar_color": random.choice(AVATAR_COLORS)})


def login_user(request):

    if request.method == 'POST':
        data = request.POST
        user = authenticate(username=data['username'], password=data['password'])

        if user is None:
            return render(request, "login.html", {"error": True})

        login(request, user)
        return redirect("home")

    return render(request, "login.html")


@login_required
def profile(request):
    return render(request, "profile.html")


@login_required
def get_users(request):
    users = User.objects.exclude(username=request.user.username)
    return render(request, "users.html", {"users": users})



@login_required
def user_chat(request, id):

    other = get_object_or_404(User, pk=id)

    chat = Chat.objects.filter(
        Q(user1 = request.user, user2 = other) | Q(user2 = request.user, user1 = other) 
    ).first()

    if chat is None:
        chat = Chat.objects.create(
            user1 = request.user,
            user2 = other
        )

    return redirect("chat", id = chat.id)



@login_required
def chat_page(request, id):
    chat = get_object_or_404(Chat, pk=id)

    chat_messages = Message.objects.filter(
        chat = chat,
        is_active = True
    ).order_by("-created_at")

    
    if chat.user1 == request.user:
        other = chat.user2
    else:
        other = chat.user1


    context = {
        "chat" : chat,
        "chat_messages": chat_messages,
        "other" : other
    }

    return render(request, "chat_page.html", context)