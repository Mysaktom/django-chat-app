# chat/models.py
from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    author = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    # TENTO ŘÁDEK PŘIDEJ:
    room = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    class Meta:
        ordering = ['timestamp']