from myApp.views import hourly_function
from celery import shared_task

@shared_task(bind=True)
def hourly_task(self):
    hourly_function()
    return "Done"