from django.apps import AppConfig


class MyWebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_web'

    def ready(self):
        import my_web.signals
