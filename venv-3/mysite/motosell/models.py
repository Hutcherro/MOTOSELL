from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from model_helpers import Choices
from django.utils.timezone import now


class Notice(models.Model):
    ALL_FUEL_TYPES = Choices({
        "benzyna": "benzyna",
        "diesel": "diesel",
        "LPG": "LPG",
    })
    title = models.TextField(max_length=50)
    description = models.TextField(max_length=100)
    production_year = models.IntegerField()
    mileage = models.IntegerField()
    cubic_capacity = models.IntegerField()
    horse_power = models.IntegerField()
    fuel_type = models.CharField(max_length=7, choices=ALL_FUEL_TYPES())
    price = models.IntegerField()
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    # user = models.CharField(max_length=100, default=None, blank=True)
    picture = models.ImageField()
    # picture = models.ImageField(upload_to='')
    # date_added = models.DateTimeField(auto_now_add=True)
    date_added = models.DateTimeField(default=now, blank=True)
    date_published = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False, blank=True)
    is_publicated = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.title

    # objects = models.Manager()
