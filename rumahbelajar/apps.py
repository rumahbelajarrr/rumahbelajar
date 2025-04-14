from django.apps import AppConfig

class AbsensiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rumahbelajar'

    def ready(self):
        import rumahbelajar.signals  # pastikan nama app-nya sesuai

