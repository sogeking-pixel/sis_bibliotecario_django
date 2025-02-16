import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config

class Command(BaseCommand):
    help = "Crea un superusuario automáticamente si no existe"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = config("DJANGO_SUPERUSER_USERNAME")
        email = config("DJANGO_SUPERUSER_EMAIL")
        password = config("DJANGO_SUPERUSER_PASSWORD")

        if username and email and password:
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username=username, email=email, password=password)
                self.stdout.write(self.style.SUCCESS(f"✅ Superusuario '{username}' creado correctamente."))
            else:
                self.stdout.write(self.style.WARNING(f"ℹ️ El superusuario '{username}' ya existe."))
