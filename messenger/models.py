from django.db import models
from django.contrib.auth.models import AbstractUser
import random



def random_avatar_color():
    colors = [
        "#5865F2",
        "#E67E22",
        "#27AE60",
        "#E84393",
        "#8E44AD",
        "#16A085",
        "#D35400",
        "#2980B9",
    ]
    return random.choice(colors)



class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
    bio = models.TextField(blank=True)
    avatar_color = models.CharField(max_length=10)

class Chat(models.Model):
    TYPES = [
        ("private", "Личный"),
        ("group", "Группа"),
        ("channel", "Канал"),
        ("saved", "Избранное"),
    ]
    type = models.CharField(max_length=10, choices=TYPES, default="private")
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="chat_avatars", null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_chats")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)



class ChatMember(models.Model):
    ROLES = [("owner", "Владелец"), ("admin", "Админ"), ("member", "Участник")]

    PERMISSIONS = {
        "add_member":         ("owner", "admin"),
        "remove_member":      ("owner", "admin"),
        "edit_group":         ("owner", "admin"),
        "delete_any_message": ("owner", "admin"),
        "set_admin":          ("owner",),
        "transfer_owner":     ("owner",),
        "delete_group":       ("owner",),
        "see_deleter":        ("owner",),
    }

    RANK = {"owner": 3, "admin": 2, "member": 1}


    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(max_length=10, choices=ROLES, default="member")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("chat", "user")

    def can(self, action):
        return self.role in self.PERMISSIONS.get(action, ())


    def can_remove(self, target):
        return (
            self.RANK[self.role] > self.RANK[target.role]
            and self.can("remove_member")
            and self.pk != target.pk
        )


    def all_permissions(self):
        return {action: self.can(action) for action in self.PERMISSIONS}







class Message(models.Model):
    file_types = [
        ("image", "Изображение"),
        ("video", "Видео"),
        ("file", "Файл")
    ]
    
    is_read = models.BooleanField(default=False)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sender")
    text = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to="files/", blank=True)
    file_type = models.CharField(max_length=20, choices=file_types, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="deleted_messages")
    is_active = models.BooleanField(default=True)



