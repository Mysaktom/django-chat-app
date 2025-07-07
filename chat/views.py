# chat/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message

@login_required
def chat_page(request):
    # Načteme posledních 25 zpráv
    messages = Message.objects.all().order_by('-timestamp')[:25][::-1]
    return render(request, 'chat/chat_page.html', {'messages': messages})