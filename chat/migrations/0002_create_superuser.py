from django.db import migrations
from django.contrib.auth.models import User

def create_superuser(apps, schema_editor):
    # Použij get_user_model pro získání aktuálního modelu uživatele
    User = apps.get_model('auth', 'User')

    # Vytvoř superuživatele, pouze pokud ještě neexistuje
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='tomtom020305' 
        )

class Migration(migrations.Migration):
    dependencies = [
        ('chat', '0001_initial'), # Ujisti se, že název odpovídá tvé první migraci
    ]
    operations = [
        migrations.RunPython(create_superuser),
    ]