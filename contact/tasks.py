from django.conf import settings
from django.core.mail import send_mail

from contact.models import Contact
from movies.celery import app

@app.task
def send_beat_email():
    user_emails = Contact.objects.only('email')
    send_mail(
        subject='Рассылка от Django Movies',
        message='Мы присылаем это сообщение ночью, чтобы пожелать Вам сладких снов :з',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=user_emails,
        fail_silently=False
    )
