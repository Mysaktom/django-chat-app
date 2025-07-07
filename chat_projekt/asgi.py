# chat_projekt/asgi.py
import os
from django.core.asgi import get_asgi_application

# NEJDŘÍVE nastavíme cestu k settings, ještě před ostatními importy z Djanga
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_projekt.settings')

# TEPRVE TEĎ, když Django ví, kde má nastavení, můžeme bezpečně importovat zbytek
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})