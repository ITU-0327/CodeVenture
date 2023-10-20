from django.apps import AppConfig


class ProgresstrackingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ProgressTracker"

    def ready(self):
        import ProgressTracker.signals
