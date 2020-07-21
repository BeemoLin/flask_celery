# -*- coding: utf-8 -*-
import json
from flask import current_app
from flask import Blueprint
from flask import jsonify
from flask import request
from app.tasks import hello, add, queue_list, get_config

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
    cfg = current_app.config
    cfg = json.dumps(cfg, indent=4, sort_keys=True, default=str)
    cfg = json.loads(cfg)
    return jsonify(cfg)


@bp.route('/celery_config')
def celery_config():
    r = get_config.delay()
    r.wait()
    cfg = json.loads(r.result)
    return jsonify(cfg)


@bp.route('/add_task')
def add_task():
    count = request.args.get('count', default=1, type=int)
    print(count)
    response = []
    for i in range(count):
        r = add.delay(1, 2)
        response.append({
            'task_id': r.task_id,
            'task': '1 + 2 = ?'
        })
    return jsonify(response)


@bp.route('/run_task')
def run_task():
    r = add.delay(1, 2)
    r.wait()
    print(r.result)
    response = {
        'task_id': r.task_id,
        'task': '1 + 2 = {}'.format(r.result)
    }
    return jsonify(response)