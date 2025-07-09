# chat/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message, Room


@login_required
def room_selection(request):
    # Teď získáme všechny objekty místností přímo
    rooms = Room.objects.all()
    return render(request, 'chat/room_selection.html', {
        'rooms': rooms
    })


@login_required
def chat_page(request, room_name):
    # Najde místnost podle jména, nebo ji VYTVOŘÍ, pokud neexistuje.
    # Toto je ta klíčová změna, která vše opraví.
    room, created = Room.objects.get_or_create(name=room_name)

    # Zbytek funkce zůstává stejný a načte zprávy pro danou místnost
    messages = room.messages.all().order_by('timestamp')[:25]
    return render(request, 'chat/chat_page.html', {
        'room_name': room.name,
        'messages': messages
    })