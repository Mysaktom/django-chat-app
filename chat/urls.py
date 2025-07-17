# chat/urls.py
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView 
from . import views

urlpatterns = [
    # Cesty pro chat
    path('chat/', views.room_selection, name='room-selection'),
    path('chat/<str:room_name>/', views.chat_page, name='chat-page'),

    # Cesty pro přihlášení a odhlášení
    path('', LoginView.as_view(template_name='chat/login_page.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # Cesty pro změnu hesla
    path(
        'password-change/',
        auth_views.PasswordChangeView.as_view(
            template_name='chat/password_change_form.html', # <- Odkaz na šablonu formuláře
            success_url=reverse_lazy('password-change-done')
        ),
        name='password-change'
    ),
    path(
        'password-change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='chat/password_change_done.html' # <- Odkaz na šablonu s potvrzením
        ),
        name='password-change-done'
    ),
    # Cesta pro uložení obsahu plátna
    path('save-canvas/<str:room_name>/', views.save_canvas, name='save-canvas'),
    # Nastavení notifikací
    path('notifications/settings/', views.notification_settings, name='notification-settings'),
]