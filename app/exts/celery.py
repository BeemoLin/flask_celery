from celery import Celery
from app import create_app

celery = Celery(__name__)


def init_celery(app=None):
    app = app or create_app()

    print('init_celery: {}'.format(app.config.get("CELERY_CONFIG", None)['broker_url']))
    celery.config_from_object(app.config.get("CELERY_CONFIG", None))

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
