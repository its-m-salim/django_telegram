from django.urls import path
from .views import *

urlpatterns = [
    path('', home_page, name='home'),
    path("login/", login_user, name="login"),
    path("registration/", registration, name="registration"),
    path("logout/", logout_user, name="logout" )
]


