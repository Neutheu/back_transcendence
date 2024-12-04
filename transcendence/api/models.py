from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    nickname = models.CharField(max_length=50, unique=True)
# Il faudra ajouter une field pour stocker l'avatar du user
    def __str__(self):
        return self.nickname # Permet qu'une instance de User soit affichee via son nickname et non <User object (id)>
    
