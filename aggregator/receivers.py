from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask, IntervalSchedule


@receiver(post_migrate)
def setup_periodic_tasks(sender, **kwargs):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.MINUTES,
    )

    PeriodicTask.objects.update_or_create(
        interval=schedule,
        name="Collect NCBA Bank Data",
        task="aggregator.tasks.collect_data_ncba",
    )
