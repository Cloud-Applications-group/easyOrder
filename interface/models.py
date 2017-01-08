from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
import pytz
from django.conf import settings
# Create your models here.

# Order status
STATUS_NEW              = 0
STATUS_PROCESSING       = 1
STATUS_FAILED           = 2
STATUS_READY            = 3
STATUS_COMPLETED        = 4


STATUS_CHOICES = (
    (STATUS_NEW,                'New'),
    (STATUS_PROCESSING,         'Processing'),
    (STATUS_FAILED,             'Failed'),
    (STATUS_READY,             'Failed'),
    (STATUS_COMPLETED,          'Completed')
)

#Popularity

STATUS_NOT_BUSY              = 0
STATUS_BUSY                  = 1
STATUS_FULL                  = 2



STATUS_POP_CHOICES = (
    (STATUS_NOT_BUSY,     'Not Busy'),
    (STATUS_BUSY,         'Busy'),
    (STATUS_FULL,         'Full'),
)


def add_now():
    return datetime.now(getattr(pytz, settings.TIME_ZONE))

class Restaurant(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, default=None)
    location_id = models.CharField("Unique Id", null=True, blank=True, default=None, max_length=4096)
    name = models.CharField("Restaurant Name", null=True, blank=True, default=None, max_length=4096)
    info = models.TextField(null=True, blank=True)
    is_available = models.BooleanField(null=False, blank=False, default=False)
    popularity = models.IntegerField(null=False, blank=False, default=STATUS_NOT_BUSY, choices=STATUS_POP_CHOICES)


class Order(models.Model):
    user = models.ForeignKey(User, null=False, blank=False)
    restaurant = models.ForeignKey(Restaurant, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    amount = models.IntegerField(null=False, blank=False)
    people = models.IntegerField(null=False, blank=False, default=1)
    status = models.IntegerField(null=False, blank=False, default=STATUS_NEW, choices=STATUS_CHOICES)
    date_time = models.DateTimeField("Submitted on", null=False, blank=True, default=add_now)
    reservation_date_time = models.TextField("Reserve time", null=False, blank=False, default='now')

class Menu(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, default=None)
    restaurant = models.ForeignKey(Restaurant, null=False, blank=False)
    content = models.TextField(null=False, blank=False)



