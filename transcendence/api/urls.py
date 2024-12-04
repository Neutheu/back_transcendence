from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.users_list, name='users_list'),
    path('users/<int:id>/', views.user_detail, name='user_detail'),
    path('users/<int:id>/update/', views.update_user, name='update_user'),
    path('games/', views.games_list, name='games_list'),
    path('games/<int:id>/', views.game_detail, name='game_detail'),
]
