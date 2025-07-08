from django.contrib import admin
from .models import Room, Message # Importujeme naše modely

# Zaregistrujeme modely, aby byly vidět v administraci
admin.site.register(Room)
admin.site.register(Message)

# Register your models here.
