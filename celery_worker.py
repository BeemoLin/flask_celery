from app.exts.celery import init_celery
from app.celery_config import celery_config
from app import create_app

celery = init_celery(celery_config)

app = create_app()
app.app_context().push()