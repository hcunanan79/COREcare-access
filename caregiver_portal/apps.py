from django.apps import AppConfig


class CaregiverPortalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'caregiver_portal'

    def ready(self):
        import caregiver_portal.signals
