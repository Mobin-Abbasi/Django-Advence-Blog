from celery import shared_task
import time


@shared_task
def sendEmail():
    time.sleep(5)
    print("email sent")
