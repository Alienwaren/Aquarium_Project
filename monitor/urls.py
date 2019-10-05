from django.urls import path

from monitor import views
from monitor.views import data_views

urlpatterns = [
    path('', views.index, name="index"),
    path('about', views.about, name="about"),
    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('user_page', views.user_page, name="user_page"),
    path('user_page/add_new_pet', views.add_new_pet, name="add_new_pet"),
    path('user_page/add_new_habitat', views.add_new_habitat, name="add_new_habitat"),
    path('user_page/habitat/<pet>/', views.habitat_page, name="habitat_page"),
    path('user_page/habitat/<pet>/manage', views.manage_habitat, name="manage_habitat"),
    path('api/add_data/<api_key>/<data_topic>/<value>', data_views.add_data_from_url, name="add_data_url")
]