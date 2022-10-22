import hashlib
import random
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User

def generate_code():
    length=8
    base = string.ascii_lowercase+string.ascii_uppercase+string.digits
    while True:
        code = ''.join(random.choices(base, k=length))
        break
    return code

def registration_mail(email, data):
    subject = f' Hi , {name} from ESCAPE '
    message = f'Your verification CODE is {verification_code} '
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email,]
    send_mail(subject, message, from_email, recipient_list)
    return verification_code