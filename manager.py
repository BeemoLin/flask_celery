from app import create_app
from flask_script import Manager
# from gevent import monkey
from app.exts.celery import init_celery

run_production = False
config_mode = 'production' if run_production else 'development'

app = create_app(config_mode)

celery = init_celery(app)

manager = Manager(app)


@manager.command
def run():
    # multi thread block problem
    # monkey.patch_all()
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    manager.run()
