from django.apps import AppConfig


class MeddyTourguidesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'meddy_tourguides'
    
    def ready(self):
        """Register signal handlers when app is ready"""
        try:
            from . import signals
            signals.register_signals()
        except Exception as e:
            print(f"Warning: Could not register signals: {str(e)}")
