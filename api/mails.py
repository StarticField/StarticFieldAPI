from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template

from django.conf import settings
from .models import *
import datetime
import random
import string

def generate_key(username):
    length=10
    base = string.ascii_letters+string.digits
    while True:
        key = username+''.join(random.choices(base,k=length))
        if not PasswordResetRequest.objects.filter(key=key).exists():
          break  
    return key

def send_reset_mail(email, username):
    key = generate_key(username)
    url = f'https://starticfield.com/reset-password?email={username}&key={key}'
    message = get_template("reset_pass.html").render({
        'username': username,
        'url': url
    })
    mail = EmailMessage(
        subject= f"Request for password reset @StarticField",
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[email],
        reply_to=[settings.EMAIL_HOST_USER],
    )
    mail.content_subtype = "html"
    return mail.send()

def send_advertisement_mail(emails):
    message = get_template("advertisement.html").render()
    mail = EmailMessage(
        subject= f"All India Student CTO Hunt competetion 2022",
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=emails,
        reply_to=[settings.EMAIL_HOST_USER],
    )
    mail.content_subtype = "html"
    return mail.send()