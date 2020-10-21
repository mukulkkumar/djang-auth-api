from django.db import models
from datetime import timedelta
from django.utils import timezone


# Create your models here.
class MobileOTP(models.Model):
    phone_num = models.CharField(max_length=20)
    otp_num = models.IntegerField(null=True, blank=True)
    create_time = models.DateTimeField(default=timezone.now())
    expiry_time = models.DateTimeField(default=timezone.now()+timedelta(minutes=5))
    is_valid = models.BooleanField(default=False)
