from django.db import models
from django.contrib.auth.models import AbstractUser




class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
    bio = models.TextField(blank=True)



class Chat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, related_name="chats1")
    user2 = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, related_name="chats2")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

class Message(models.Model):
    file_types = [
        ("image", "Изображение"),
        ("video", "Видео"),
        ("file", "Файл")
    ]
    is_read = models.BooleanField(default=False)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to="files/", blank=True)
    file_type = models.CharField(max_length=20, choices=file_types, default="file")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

