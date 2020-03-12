from django.conf import settings
from django.core.mail import send_mail

from movies.celery import app

@app.task
def send(user_email):
    send_mail(
        subject='Header',
        message='message 2',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False
    )
