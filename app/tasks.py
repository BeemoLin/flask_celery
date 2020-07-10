import json
from time import sleep
from flask import current_app, jsonify
from app.exts.celery import celery


def queue_list():
    # Inspect all nodes.
    i = celery.control.inspect()
    queue = i.reserved()
    current_app.logger.info("workers = {}".format(list(queue.keys())))
    return queue


@celery.task(name='hello')
def hello():
    print("Hello there")


@celery.task
def add(a, b):
    sleep(10)
    print('{} + {} = {}'.format(a, b, (a + b)))


@celery.task
def get_config():
    cfg = current_app.config
    cfg = json.dumps(cfg, indent=4, sort_keys=True, default=str)
    return str(cfg)
