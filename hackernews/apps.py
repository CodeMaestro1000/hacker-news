from django.apps import AppConfig


class HackernewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hackernews'

    def ready(self):
        from newsUpdater import updater

        updater.start()
