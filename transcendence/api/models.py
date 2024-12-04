from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    nickname = models.CharField(max_length=50, unique=True)
# Il faudra ajouter une field pour stocker l'avatar du user
    def __str__(self):
        return self.nickname # Permet qu'une instance de User soit affichee via son nickname et non <User object (id)>
    
class Game(models.Model):
    player1 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='games_as_player1') # on_delete=models.SET_NULL : Si un utilisateur est supprimé, ce champ sera null.
    player2 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='games_as_player2')
    score_player1 = models.IntegerField(default=0)
    score_player2 = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player1} vs {self.player2} - {self.score_player1}:{self.score_player2}"
