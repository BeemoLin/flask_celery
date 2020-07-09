import os
from flask import Flask
from werkzeug.utils import import_string
from app.config import app_config
from app.celery_config import celery_config

blueprints = [
    ("app.routes.root:bp", "/"),
    ("app.routes.admin:bp", "/admin"),
]


extensions = [
    ('app.exts.celery:init_celery', celery_config)
]


def _access_control(response):
    """
    CORS
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,HEAD,PUT,PATCH,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Max-Age'] = 86400
    return response


def create_app(config_name='development'):

    app = Flask(__name__)
    # 添加配置
    config = app_config[config_name]
    app.config.from_object(config)

    # 解决跨域
    app.after_request(_access_control)

    # init extensions
    for ext_name, cfg in extensions:
        init_ext = import_string(ext_name)
        init_ext(cfg)

    # register blue print
    for bp_name, prefix in blueprints:
        bp = import_string(bp_name, silent=False)
        app.register_blueprint(bp, url_prefix=prefix)
    return app
