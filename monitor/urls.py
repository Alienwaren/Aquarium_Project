from django.contrib import admin
from django.urls import path

from monitor import views

urlpatterns = [
    path('', views.index, name="index"),
    path('about', views.about, name="about"),
    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('user_page', views.user_page, name="user_page")
]