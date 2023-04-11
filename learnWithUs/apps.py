from django.apps import AppConfig


class LearnwithusConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'learnWithUs'
    def ready(self):
        import learnWithUs.signals
