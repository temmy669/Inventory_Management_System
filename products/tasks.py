from celery import shared_task

@shared_task
def test_celery_task():
    print("Celery task is running!")
    return "Task completed!"

@shared_task
def add(x, y):
    print(f'Task started with arguments: {x}, {y}')
    return x + y
