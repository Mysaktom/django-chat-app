# chat_projekt/urls.py
from django.contrib import admin
from django.urls import path, include # Ujisti se, že je zde 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    # TENTO ŘÁDEK PŘIDEJ:
    path('', include('chat.urls')),
]