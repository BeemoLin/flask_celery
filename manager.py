from app import create_app
from flask_script import Manager
from gevent import monkey

# multi thread block problem
monkey.patch_all()

app = create_app()
manager = Manager(app)


@manager.command
def run():
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    manager.run()
