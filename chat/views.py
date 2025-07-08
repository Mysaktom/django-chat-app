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
    all_rooms = Message.objects.values_list('room', flat=True).distinct()
    
    # Krok 2: Vyčistíme je a odstraníme duplikáty v Pythonu pro jistotu
    # Ořízne mezery, převede na malá písmena a vezme jen unikátní hodnoty
    cleaned_rooms = sorted(list(set(r.strip().lower() for r in all_rooms if r)))
    
    return render(request, 'chat/room_selection.html', {
        'rooms': cleaned_rooms
    })

@login_required
def chat_page(request, room_name):
    # Najdeme objekt místnosti, nebo vrátíme chybu 404, pokud neexistuje
    try:
        room = Room.objects.get(name=room_name)
    except Room.DoesNotExist:
        # Zde by se hodilo zobrazit hezčí chybovou stránku, ale pro teď stačí
        from django.http import Http404
        raise Http404("Místnost neexistuje")

    messages = room.messages.all().order_by('timestamp')[:25]
    return render(request, 'chat/chat_page.html', {
        'room_name': room.name,
        'messages': messages
    })