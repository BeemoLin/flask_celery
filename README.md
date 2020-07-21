# flask_celery_blueprint

## launch

### start `redis`
```
docker-compose up -d
```
### start `flask` with `celery worker`
```
python manager.py run
```

## optional
### start `celery worker` only
```
python manager.py start_worker
```
