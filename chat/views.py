# chat/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message, Room, User


@login_required
def room_selection(request):
    # Teď získáme všechny objekty místností přímo
    rooms = Room.objects.all()
    return render(request, 'chat/room_selection.html', {
        'rooms': rooms
    })

# Zobrazí stránku pro výběr místnosti
@login_required
def room_selection(request):
    # Krok 1: Získáme všechny unikátní názvy místností z databáze
    rooms = Room.objects.all()
    
    return render(request, 'chat/room_selection.html', {
        'rooms': rooms
    })

@login_required
def chat_page(request, room_name):
    # Najdeme objekt místnosti, nebo vrátíme chybu 404, pokud neexistuje
    room, created = Room.objects.get_or_create(name=room_name)

    messages = room.messages.all().order_by('timestamp')[:25]
    return render(request, 'chat/chat_page.html', {
        'room_name': room.name,
        'messages': messages
    })
