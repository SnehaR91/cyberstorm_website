# users/urls.py
from django.urls import path
from .views import register_team, login_team, dashboard, logout_team

urlpatterns = [
    path('register/', register_team, name='register'),
    path('login/', login_team, name='login'),
    path('logout/', logout_team, name='logout'),
]
