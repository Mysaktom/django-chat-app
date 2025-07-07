# chat/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message

# TUTO FUNKCI PŘIDEJ:
@login_required
def room_selection(request):
    return render(request, 'chat/room_selection.html')

@login_required
def chat_page(request, room_name): # <- Tuto funkci už tam máš, jen ji upravíme
    # Zde bychom měli filtrovat zprávy podle room_name, ale to teď neřešme
    messages = Message.objects.all().order_by('-timestamp')[:25][::-1]
    return render(request, 'chat/chat_page.html', {
        'room_name': room_name,
        'messages': messages
    })