# chat/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('chat/', views.chat_page, name='chat-page'),
    path('', LoginView.as_view(template_name='chat/login_page.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]