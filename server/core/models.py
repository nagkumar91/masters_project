from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from rest_framework.authtoken.models import Token


class AppUser(AbstractUser):
    REQUIRED_FIELDS = ['email']

    verified = models.BooleanField(default=False)
    unique_code = models.CharField(max_length=255, null=True, blank=True)
    phone_type = models.CharField(max_length=10, choices=settings.PHONE_TYPE, null=True, blank=True)
    push_notification_id = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = get_random_string(length=25)
        super(AppUser, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.get_full_name()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class RideRequest(models.Model):
    requested_by = models.ForeignKey(AppUser, related_name='ride_requests')
    pickup_address = models.TextField(null=True, blank=True)
    pickup_latitude = models.DecimalField(max_digits=14, decimal_places=10)
    pickup_longitude = models.DecimalField(max_digits=14, decimal_places=10)
    drop_off_address = models.TextField(null=True, blank=True)
    drop_off_latitude = models.DecimalField(max_digits=14, decimal_places=10)
    drop_off_longitude = models.DecimalField(max_digits=14, decimal_places=10)
    request_time = models.DateTimeField(auto_now_add=True)
    picked_up_at = models.DateTimeField(null=True, blank=True)
    droped_off_at = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.requested_by.__unicode__()

