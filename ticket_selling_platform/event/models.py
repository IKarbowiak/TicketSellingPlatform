from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=100)
    datetime = models.DateTimeField()
    description = models.TextField()
