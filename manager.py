from app import create_app
from flask_script import Manager
# from gevent import monkey

from celery import current_app
from celery.bin import worker


run_production = False
config_mode = 'production' if run_production else 'development'

app = create_app(config_mode)

manager = Manager(app)


@manager.command
def run():
    # multi thread block problem
    # monkey.patch_all()

    app.run(host='0.0.0.0', port=5000)


@manager.command
def start_worker():
    application = current_app._get_current_object()
    celery_worker = worker.worker(app=application)
    celery_config = app.config.get("CELERY_CONFIG", None)
    options = {
        'broker': celery_config['broker_url'] if celery_config['broker_url'] is None else '0.0.0.0',
        'loglevel': celery_config['loglevel'] if celery_config['loglevel'] is None else 'INFO',
        'traceback': celery_config['traceback'] if celery_config['traceback'] is None else True,
    }

    celery_worker.run(**options)


if __name__ == '__main__':
    manager.run()
