import os


class Config:
    # celery config
    timezone = 'Asia/Taipei'
    result_accept_content = ['json']
    task_serializer = 'json'
    result_serializer = 'json'
    result_backend = "redis://{}:6379".format(os.environ.get("REDIS_HOST", ''))
    broker_url = "redis://{}:6379".format(os.environ.get("REDIS_HOST", ''))


celery_config = Config()
