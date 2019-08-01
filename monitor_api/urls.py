from django.urls import path

from monitor_api import views

urlpatterns = [
    path('', views.index_api, name="test")
]