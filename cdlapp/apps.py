from django.apps import AppConfig


class CdlappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cdlapp"
    verbose_name = 'cdlapp'  # Change this to your desired name

    def ready(self):
        # everytime server restarts
        import cdlapp.signals
