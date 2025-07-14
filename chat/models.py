# chat/models.py
from django.db import models
from django.contrib.auth.models import User

# 1. Nejprve definujeme model Room
class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    canvas_content = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# 2. Až potom definujeme model Message, který na Room odkazuje
class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.author.username}: {self.content[:20]}'

    class Meta:
        ordering = ['timestamp']


