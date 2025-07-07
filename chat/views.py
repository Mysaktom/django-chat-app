# chat/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message

# TUTO FUNKCI PŘIDEJ:
@login_required
def room_selection(request):
    return render(request, 'chat/room_selection.html')

@login_required
def chat_page(request, room_name):
    # UPRAVENO: filtrujeme zprávy jen pro danou místnost
    messages = Message.objects.filter(room=room_name).order_by('timestamp')[:25]
    return render(request, 'chat/chat_page.html', {
        'room_name': room_name,
        'messages': messages
    })