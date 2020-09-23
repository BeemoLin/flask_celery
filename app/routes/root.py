# -*- coding: utf-8 -*-
import json, csv
from flask import current_app
from flask import Blueprint
from flask import jsonify
from flask import request
from app.tasks import hello, add, queue_list, get_config
from app.models.yolov4.train import create_log_dir, get_train_log_path

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
    epoch = request.args.get('epoch', default=5, type=int)
    log_dir = create_log_dir()
    r = add.delay(log_dir, epoch)
    response = {
        'task_id': r.task_id,
        'log_dir': log_dir,
        'epoch': epoch
    }
    return jsonify(response)


@bp.route('/read_log')
def read_log():
    log_path = request.args.get('log_path', default=None)
    if log_path is None:
        return "ERROR: log not exist"

    train_log_path = get_train_log_path(log_path)

    with open(train_log_path, mode="r") as files:
        dict_reader = csv.DictReader(files)
        csv_dict = json.dumps([row for row in dict_reader], indent=2)
    
    return csv_dict