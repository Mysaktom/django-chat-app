# chat/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Room, Message
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

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
    Zobrazí konkrétní chatovací místnost a její obsah.
    Pokud místnost neexistuje, vytvoří ji.
    """
    room, created = Room.objects.get_or_create(name=room_name)
    messages = room.messages.all().order_by('timestamp')
    
    return render(request, 'chat/chat_page.html', {
        'room_name': room.name,
        'messages': messages,
        'canvas_content': room.canvas_content
    })

@require_POST
@login_required
def save_canvas(request, room_name):
    """
    Uloží aktuální stav plátna pro danou místnost.
    """
    try:
        room = Room.objects.get(name=room_name)
        data = json.loads(request.body)
        room.canvas_content = data.get('content')
        room.save()
        return JsonResponse({'status': 'ok'})
    except Room.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=404)