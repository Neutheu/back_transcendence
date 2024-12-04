from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
import json
from api.models import Game

User = get_user_model() # retourne le modele User definit par AUTH_USER_MODEL

@csrf_exempt # desactive la methode d'authentification par defaut de django car on utilise JWT
def users_list(request):
    if request.method == 'GET':
        users = list(User.objects.values('id', 'username', 'nickname'))  # Liste des utilisateurs.
        return JsonResponse(users, safe=False, status=200) # safe=false permet d'envoyer une reponse JSON qui n'est pas necessairement un dictionnaire
    elif request.method == 'POST':
        data = json.loads(request.body)
        user = User.objects.create_user( # method de user qui hache le mdp, valide les infos utilisateur et cree le user dans la DB
            username=data['username'], password=data['password'], nickname=data['nickname']
        )
        return JsonResponse({'id': user.id, 'username': user.username}, status=201)

@csrf_exempt
def games_list(request):
    if request.method == 'GET':
        games = list(Game.objects.values('id', 'player1__nickname', 'player2__nickname', 'score_player1', 'score_player2', 'created_at'))
        return JsonResponse(games, safe=False, status=200)
    elif request.method == 'POST':
        data = json.loads(request.body)
        game = Game.objects.create( # methode qui cree l'instance et l'enregistre automatiquement dans la base de donnee
            player1_id=data['player1_id'],
            player2_id=data['player2_id'],
            score_player1=data['score_player1'],
            score_player2=data['score_player2']
        )
        return JsonResponse({'id': game.id}, status=201)
