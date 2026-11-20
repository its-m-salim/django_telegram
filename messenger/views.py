import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Q
from django.utils import timezone

AVATAR_COLORS = ["#e17076", "#faa774", "#a695e7", "#7bc862", "#6ec9cb", "#65aadd", "#ee7aae"]


@login_required
def home_page(request):
    chats = Chat.objects.filter(members__user=request.user).order_by("-created_at")

    items = []
    for chat in chats:
        other_member = chat.members.exclude(user=request.user).select_related("user").first()
        if other_member and chat.type == "private":
            other = other_member.user
        else:
            other = None

        last_message = Message.objects.filter(
            chat=chat, is_active=True
        ).exclude(text__isnull=True).exclude(text="").order_by("-created_at").first()

        items.append({"chat": chat, "other": other, "last_message": last_message})

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
    query = request.GET.get("q", "").strip()
    users = User.objects.exclude(pk=request.user.pk)

    if query:
        users = users.filter(
            Q(first_name__icontains=query) | Q(username__icontains=query)
        )

    return render(request, "users.html", {"users": users})



@login_required
def user_chat(request, id):
    other = get_object_or_404(User, pk=id)

    chat = Chat.objects.filter(
        type="private", members__user=request.user
    ).filter(members__user=other).first()

    if chat is None:
        chat = Chat.objects.create(type="private", created_by=request.user)
        ChatMember.objects.create(chat=chat, user=request.user, role="member")
        ChatMember.objects.create(chat=chat, user=other, role="member")

    return redirect("chat", id=chat.id)









@login_required
def chat_page(request, id):
    chat = get_object_or_404(Chat, pk=id)
    if not chat.members.filter(user=request.user).exists():
        return redirect("home")

    chat_messages = Message.objects.filter(chat=chat).order_by("created_at")
    
    other_member = chat.members.exclude(user=request.user).select_related("user").first()
    other = other_member.user if other_member else None

    context = {
        "chat" : chat,
        "chat_messages": chat_messages,
        "other" : other
    }

    if request.method == 'POST':

        files = request.FILES
        file = None
        file_type = None
        if files.get("image"):
            file = files['image']
            file_type = "image"
        elif files.get("video"):
            file = files['video']
            file_type = "video" 
        elif files.get("file"):
            file = files['file']
            file_type = "file"           
    


        if request.POST.get("message-text") or file:
            Message.objects.create(
                chat = chat,
                sender = request.user,
                text = request.POST['message-text'],
                file = file,
                file_type = file_type 
            )
        return redirect("chat", chat.id)

    return render(request, "chat_page.html", context)





@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        data = request.POST
        user.first_name = data['first_name']
        if User.objects.filter(username=data['username']).exclude(pk=user.pk).exists():
            return render(request, "edit_profile.html", {"error": True})

        if request.FILES.get("avatar"):
            user.avatar = request.FILES["avatar"]

        user.bio = request.POST.get("bio")
        user.username = data['username']
        user.save()
        return redirect("home")

    return render(request, "edit_profile.html")



@login_required
def edit_message(request, message_id):
    message = get_object_or_404(
        Message,
        pk=message_id,
        sender=request.user,
        is_active=True
    )

    if request.method == "POST":
        text = request.POST.get("text", "").strip()

        if text:
            message.text = text
            message.updated_at = timezone.now()
            message.save()

            return redirect("chat", id=message.chat.id)

    return render(request, "edit_message.html", {"message": message})



@login_required
def delete_message(request, message_id):
    message = get_object_or_404(
        Message,
        pk=message_id,
        sender=request.user,
        is_active=True
    )

    if request.method == "POST":
        message.is_active = False
        message.save()

    return redirect("chat", id=message.chat.id)



@login_required
def user_profile(request,chat_type,  id):
    person = get_object_or_404(User, pk=id) if chat_type == "private" else get_object_or_404(Chat, pk =id)
    return render(request, "user_profile.html", {"person": person})




@login_required
def create_group(request):
    if request.method == 'POST':
        data = request.POST
        members = request.POST.getlist("members")

        if not data.get('title').strip():
            return render("group_form", {"error": "Имя группы не может быть пустым."})

        if not members or len(members) < 1:
            return render("group_form", {"error": "Нужно выбрать хотья бы одного участника"}) 


        chat = Chat.objects.create(
            title = data['title'],
            description = data.get("caption"),
            created_by = request.user,
            type = "group",
            avatar = request.FILES.get("avatar")
        )

        ChatMember.objects.create(
            chat = chat,
            user = request.user,
            role = "owner"
        )

        for member in members:
            ChatMember.objects.create(
                chat = chat,
                user = get_object_or_404(User, pk = member),
                role = "member"
            )
        return redirect("chat", id=chat.id)

    users = User.objects.exclude(pk = request.user.id)
    return render(request, "group_form.html", {"users": users})