from django.apps import AppConfig
from django.contrib.auth import get_user_model
from decouple import config


class AdministractionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'administraction'
    def ready(self):
        
        User = get_user_model()
        
        username = config("DJANGO_SUPERUSER_USERNAME")
        email = config("DJANGO_SUPERUSER_EMAIL")
        password = config("DJANGO_SUPERUSER_PASSWORD")

        print(username, email, password)
        
        if username and email and password:
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username=username, email=email, password=password)
                print(f"Superusuario fue creado correctamente.")
            else:
                print(f"ℹ️ El superusuario ya existe.") 
