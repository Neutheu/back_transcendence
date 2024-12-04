from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
import json
from api.models import Game

User = get_user_model() # retourne le modele User definit par AUTH_USER_MODEL

######## URL: users/ , ENDPOINTS: GET | POST ############

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
    return JsonResponse({'error': 'Method not allowed'}, status=405)

        #TEST AVEC CURL :
        # Créer un utilisateur.
        # curl -X POST http://127.0.0.1:8000/api/users/ -H "Content-Type: application/json" -d '{"username": "test", "password": "1234", "nickname": "tester"}'

        # Lister les utilisateurs.
        # curl http://127.0.0.1:8000/api/users/

######## URL: users/id/ , ENDPOINTS: GET ############

def user_detail(request, id):
    if request.method == 'GET':
        user = get_object_or_404(User, id=id)
        response_data = {
            'id': user.id,
            'username': user.username,
            'nickname': user.nickname,
        }
        return JsonResponse(response_data, status=200)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

        #TEST:
        # curl http://127.0.0.1:8000/api/users/1/

######## URL: users/id/update/ , ENDPOINTS: PUT ############

@csrf_exempt 
def update_user(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'PUT':
        data = json.loads(request.body)
        if 'username' in data:
            user.username = data['username']
        if 'nickname' in data:
            user.nickname = data['nickname']
        if 'password' in data:
            user.set_password(data['password'])
        user.save()
        response_data = {
            'id': user.id,
            'username': user.username,
            'nickname': user.nickname,
        }
        return JsonResponse(response_data, status=200)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

    #TEST: curl -X PUT http://127.0.0.1:8000/api/users/1/update/ -H "Content-Type: application/json" -d '{"username": "new_username", "password": "123454", "nickname": "new_nickname"}'

######## URL: games/ , ENDPOINTS: GET | POST ############

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
    return JsonResponse({'error': 'Method not allowed'}, status=405)
    
        #TEST AVEC CURL:
        # curl -X POST http://127.0.0.1:8000/api/games/ -H "Content-Type: application/json" -d '{"player1_id": "1", "player2_id": "2", "score_player1":"21", "score_player2":"232"}'
        # curl http://127.0.0.1:8000/api/games/ 

######## URL: games/id/ , ENDPOINTS: GET ############

def game_detail(request, id):
    if request.method == 'GET':
        game = get_object_or_404(Game, id=id)
        response_data = {
            'id': game.id,
            'player1': {
                'id': game.player1.id,
                'nickname': game.player1.nickname,
            },
            'player2': {
                'id': game.player2.id,
                'nickname': game.player2.nickname,
            },
            'score_player1': game.score_player1,
            'score_player2': game.score_player2,
            'created_at': game.created_at.isoformat(),  # Format reconnaissable en JSON
        }
        return JsonResponse(response_data, status=200)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

        #TEST:
        # curl http://127.0.0.1:8000/api/games/1/