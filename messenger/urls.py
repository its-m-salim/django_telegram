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
    path("chat/<int:id>/", chat_page, name="chat"),
    path("edit_profile/", edit_profile, name="edit_profile"),
    path("edit_message/<int:message_id>/", edit_message, name="edit_message"),
    path("delete_message/<int:message_id>/", delete_message, name="delete_message"),
    path("user/<int:id>/", user_profile, name="user_profile"),
    path("group_form/", create_group, name="group_form"),
    path("chat_profile/<int:id>/", group_profile, name="group_profile" ),
    path("leave_group/<int:id>/", leave_group, name="leave_group"),
    path("add_members/<int:id>/", add_members, name="add_members"),
    path("remove_member/<int:chat_id>/<int:member_id>/", remove_member, name="remove_member")
]


