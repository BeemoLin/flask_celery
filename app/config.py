import os


class Config:

import os


class Config:
    # celery config

    CELERY_CONFIG = {
        'timezone': 'Asia/Taipei'
        'result_accept_content': ['json']
        'task_serializer': 'json'
        'result_serializer': 'json'
        'result_backend': "redis://{}:6379".format(os.environ.get("REDIS_HOST", ''))
        'broker_url': "redis://{}:6379".format(os.environ.get("REDIS_HOST", ''))
    }


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
