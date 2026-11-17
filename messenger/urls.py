from django.urls import path
from .views import *

urlpatterns = [
    path('', home_page, name='home'),
    path("login/", login_user, name="login"),
    path("registration/", registration, name="registration"),
    path("logout/", logout_user, name="logout" ),
    path("profile/", profile, name="profile"),
    path("users/", get_users, name="users"),
    path("user_chat/<int:id>/",user_chat, name="user_chat"),
    path("chat/<int:id>/", chat_page, name="chat")
]




