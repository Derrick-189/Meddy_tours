from django.apps import AppConfig


class MeddyTourguidesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'meddy_tourguides'
<<<<<<< HEAD
    
    def ready(self):
        """Register signal handlers when app is ready"""
        try:
            from . import signals
            signals.register_signals()
        except Exception as e:
            print(f"Warning: Could not register signals: {str(e)}")
=======
>>>>>>> 6e674a3e4db70d9c170fa53eccbc7b2fa29be6db
