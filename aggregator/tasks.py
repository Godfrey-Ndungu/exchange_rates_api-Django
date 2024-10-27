from celery import shared_task
from .services.collect_data import CollectData


@shared_task
def collect_data_ncba():
    collector = CollectData("NCBA")
    collector()
