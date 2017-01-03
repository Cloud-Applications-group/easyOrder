from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
# Create your models here.

# Order status
STATUS_NEW              = 0
STATUS_PROCESSING       = 1
STATUS_FAILED           = 2
STATUS_COMPLETED        = 3


STATUS_CHOICES = (
    (STATUS_NEW,                'New'),
    (STATUS_PROCESSING,         'Processing'),
    (STATUS_FAILED,             'Failed'),
    (STATUS_COMPLETED,          'Completed')
)

# Ratings
RATING_UNRATED = 0
RATING_CHOICES = (
    (RATING_UNRATED, 'Unrated'),
    (1,              '1'),
    (2,              '2'),
    (3,              '3'),
    (4,              '4'),
    (5,              '5')
)


class Restaurant(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, default=None)
    name = models.CharField("Restaurant Name", null=True, blank=True, default=None, max_length=4096)
    info = models.TextField(null=True, blank=True)
    rating = models.IntegerField(null=False, blank=False, default=RATING_UNRATED, choices=RATING_CHOICES)

    def __unicode__(self):
        return u'%s' % self.name


class Order(models.Model):
    user = models.ForeignKey(User, null=False, blank=False)
    restaurant = models.ForeignKey(Restaurant, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    amount = models.IntegerField(null=False, blank=False)
    status = models.IntegerField(null=False, blank=False, default=STATUS_NEW, choices=STATUS_CHOICES)

    def __unicode__(self):
        return u'%s' % self.name

class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
