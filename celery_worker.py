from app.exts.celery import init_celery
from app import create_app

app = create_app()
app.app_context().push()

celery = init_celery(app)
