from django.db import models
from django.contrib.auth.models import User

# NOVÝ MODEL PRO MÍSTNOSTI
class Room(models.Model):
    name = models.CharField(max_length=255, unique=True) # Jméno místnosti je unikátní

    def __str__(self):
        return self.name

# UPRAVENÝ MODEL PRO ZPRÁVY
class Message(models.Model):
    # Propojení s modelem Room. on_delete=models.CASCADE znamená,
    # že když smažeš místnost, smažou se i všechny její zprávy.
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username}: {self.content[:20]}'

    class Meta:
        ordering = ['timestamp']