import os
from kombu import Exchange, Queue

class Config:
    DEFAULT_HOST_IP = '127.0.0.1'
    exchange_topic_events = Exchange(name='topic_events', type='topic')
    CELERY_CONFIG = {
        'timezone': 'Asia/Taipei',
        'result_accept_content': ['json'],
        'task_serializer': 'json',
        'result_serializer': 'json',
        # 'broker_url': "redis://{}:6379".format(os.environ.get("REDIS_HOST", DEFAULT_HOST_IP)),
        'broker_url': "amqp://guest:guest@{}:5672//".format(os.environ.get("REDIS_HOST", DEFAULT_HOST_IP)),
        'result_backend': "redis://{}:6379".format(os.environ.get("REDIS_HOST", DEFAULT_HOST_IP)),

        'celery_queues': [
            Queue('placeholder', exchange_topic_events, 'placeholder'),
        ],
        'celery_imports': ['topic_events.task'],
        
        # worker config
        'loglevel': 'INFO',
        'traceback': True,
        'concurrency': 2
    }


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
