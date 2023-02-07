from django.core.mail import send_mail
import random
from django.conf import settings
from .models import User

def send_otp_via_mail(email):
    subject ="Your account verification email"
    otp = random.randint(1000,9999)
    message = f'otp is {otp}'
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject,message, email_from,[email])
    user = User.objects.get(email= email)
    user.otp = otp
    user.save()