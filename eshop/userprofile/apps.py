from django.apps import AppConfig


class UserprofileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userprofile'

class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        import users.signals
