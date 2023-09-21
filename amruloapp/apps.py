from django.apps import AppConfig


class AmruloappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "amruloapp"

    def ready(self):
        # everytime server restarts
        import amruloapp.signals
