from celery import shared_task


@shared_task
def debug_task():
    pass  # print('My first Celery Task')
