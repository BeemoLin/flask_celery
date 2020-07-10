from celery import Celery

celery = Celery('tasks')


def init_celery(app):
    celery.config_from_object(app.config.CELERY_CONFIG)
    return celery
