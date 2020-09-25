import os

from app import create_app
from flask_script import Manager
# from gevent import monkey

from celery import current_app
from celery.bin import worker

run_production = True
config_mode = 'production' if run_production else 'development'

app = create_app(config_mode)

manager = Manager(app)


class CeleryWorkers:
    proc = None

    def __init__(self):
        # for celery on windows bug
        os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

    def __enter__(self):
        import subprocess

        self.proc = subprocess.Popen(
            ["python", "manager.py", "start_worker"],
            shell=False,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE)

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("\nworker: Celery worker will shutdown after restore tasks \n")
        # self.proc.kill()


@manager.command
def start_worker():
    application = current_app._get_current_object()
    celery_worker = worker.worker(app=application)
    celery_config = app.config.get("CELERY_CONFIG", None)
    options = {
        'broker': celery_config['broker_url'] if celery_config['broker_url'] is None else '0.0.0.0',
        'loglevel': celery_config['loglevel'] if celery_config['loglevel'] is None else 'INFO',
        'traceback': celery_config['traceback'] if celery_config['traceback'] is None else True,
        'concurrency': celery_config['concurrency'] if celery_config['concurrency'] is None else 1,
        'pool': celery_config['pool'] if celery_config['pool'] is None else 'solo',
    }

    celery_worker.run(**options)


@manager.command
def run():
    # multi thread block problem
    # monkey.patch_all()

    with CeleryWorkers():
        app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    manager.run()
