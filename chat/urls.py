# chat/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # Stránka pro výběr místnosti (např. /chat/)
    path('chat/', views.room_selection, name='room-selection'),
    
    # Stránka pro konkrétní chatovací místnost (např. /chat/obecny-pokec/)
    path('chat/<str:room_name>/', views.chat_page, name='chat-page'),
    
    # Přihlašovací stránka (/)
    path('', LoginView.as_view(template_name='chat/login_page.html'), name='login'),
    
    # Odhlášení
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]