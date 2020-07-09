# -*- coding: utf-8 -*-
import os
from flask import Blueprint
from flask import jsonify
from app.tasks import hello, add, get_redis_host, queue_list

bp = Blueprint('root', __name__)


@bp.route('/')
def index():
    return "Wellcome to VIZURO."


@bp.route('/say_hello')
def say_hello():
    hello()
    return 'hello'


@bp.route('/tasks')
def tasks():
    r = queue_list()
    return jsonify(r)


@bp.route('/config')
def config():
    return 'REDIS_HOST = {}'.format(os.environ.get("REDIS_HOST", ''))


@bp.route('/celery_config')
def celery_config():
    r = get_redis_host.delay()
    r.wait()
    return 'celery:REDIS_HOST = {}'.format(r.result)


@bp.route('/add_task')
def add_task():
    r = add.delay(1, 2)
    response = {
        'task_id': r.task_id,
        'task': '1 + 2 = ?'
    }
    return jsonify(response)
