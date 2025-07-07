# chat_projekt/asgi.py
import os
from django.core.asgi import get_asgi_application

# Krok 1: Jako úplně první věc nastavíme cestu k settings.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_projekt.settings')

# Krok 2: Připravíme a "probudíme" Django pro HTTP provoz.
# Tím se zajistí, že všechny aplikace a modely jsou správně načtené.
django_asgi_app = get_asgi_application()

# Krok 3: Teprve TEĎ, když je Django plně připravené, importujeme zbytek.
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,  # Použijeme už připravenou Django aplikaci
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})