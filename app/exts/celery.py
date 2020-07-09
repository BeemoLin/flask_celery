from celery import Celery
# from app.celery_config import config

celery = Celery('tasks')


def init_celery(config):
    celery.config_from_object(config)
    return celery
