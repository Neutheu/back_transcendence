from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.users_list, name='users_list'),
    path('games/', views.games_list, name='games_list'),
]
