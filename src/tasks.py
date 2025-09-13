import time

from src.celery_app import celery

@celery.task(name="test_task")
def test_task(time_towait, res):
    time.sleep(time_towait)
    return res