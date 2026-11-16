from django.db import models
from django.contrib.auth.models import AbstractUser




class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars', null=True)
    bio = models.TextField()


class Chat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)


class Attachment(models.Model):

    file_types = [
        ("image", "Изображение"),
        ("video", "Видео"),
        ("file", "Файл")
    ]
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    file = models.FileField(upload_to="files/")
    file_type = models.CharField(max_length=20, choices=file_types, default="file")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

