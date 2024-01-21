from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    image = models.ImageField(upload_to="users_images", null=True,blank=True)
    is_verified = models.BooleanField(default=False)

class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateField()

    def __str__(self):
        return f"EmailVerification object {self.user.email}" 
    
    def send_verification_email(self):

        link = reverse( 'users:email_verification', kwargs={'email' : self.user.email, 'code' : self.code} )
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подтверждение учётной записи для {self.user.username}'
        message = 'Для подтверждения учётной записи  для {} перейдите по ссылке: {}'.format(self.user.username, verification_link )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return datetime.now().date() >= self.expiration

