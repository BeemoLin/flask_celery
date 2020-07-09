import os
from time import sleep
from app.exts.celery import celery


def queue_list():
    # Inspect all nodes.
    i = celery.control.inspect()
    queue = i.reserved()
    queue_list = list(value for key, value in queue.items())[0]
    return queue_list


@celery.task(name='hello')
def hello():
    print("Hello there")


@celery.task
def add(a, b):
    sleep(10)
    print('{} + {} = {}'.format(a, b, (a + b)))


@celery.task
def get_redis_host():
    print(os.environ.get("REDIS_HOST", ''))
    return os.environ.get("REDIS_HOST", '')
