from django.apps import AppConfig


class AggregatorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "aggregator"

    def ready(self):
        import aggregator.receivers # noqa
