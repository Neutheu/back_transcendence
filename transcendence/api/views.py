from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
import json

User = get_user_model() # retourne le modele User definit par AUTH_USER_MODEL

@csrf_exempt # desactive la methode d'authentification par defaut de django car on utilise JWT
def users_list(request):
    if request.method == 'GET':
        users = list(User.objects.values('id', 'username', 'nickname'))  # Liste des utilisateurs.
        return JsonResponse(users, safe=False, status=200)
    elif request.method == 'POST':
        data = json.loads(request.body)
        user = User.objects.create_user(
            username=data['username'], password=data['password'], nickname=data['nickname']
        )
        return JsonResponse({'id': user.id, 'username': user.username}, status=201)

