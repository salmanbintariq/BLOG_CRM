from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

def ready(self):
    import users.signals  # Replace 'your_app_name' with the actual name of your app
