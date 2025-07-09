from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Room, Message

@login_required
def room_selection(request):
    """
    Zobrazí stránku pro výběr místnosti a seznam již existujících místností.
    """
    rooms = Room.objects.all()
    return render(request, 'chat/room_selection.html', {
        'rooms': rooms
    })

@login_required
def chat_page(request, room_name):
    """
    Zobrazí konkrétní chatovací místnost.
    Pokud místnost neexistuje, vytvoří ji.
    """
    # Najde místnost podle jména, nebo ji VYTVOŘÍ, pokud neexistuje.
    room, created = Room.objects.get_or_create(name=room_name)

    # Načte zprávy jen pro danou místnost
    messages = room.messages.all().order_by('timestamp')
    
    return render(request, 'chat/chat_page.html', {
        'room_name': room.name,
        'messages': messages
    })