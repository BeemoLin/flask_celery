import json
from time import sleep
from flask import current_app, jsonify
from app.exts.celery import celery


def queue_list():
    # Inspect all nodes.
    i = celery.control.inspect()
    queue = i.reserved()
    print(i.scheduled())
    print(i.active())
    return queue


@celery.task(name='hello')
def hello():
    print("Hello there")


@celery.task
def add(a, b):
    sleep(5)
    print('{} + {} = {}'.format(a, b, (a + b)))
    return a + b


@celery.task
def get_config():
    cfg = current_app.config
    cfg = json.dumps(cfg, indent=4, sort_keys=True, default=str)
    return str(cfg)
