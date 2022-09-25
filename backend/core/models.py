from django.db import models
from django.contrib.auth.models import User


class PestTrap(models.Model):
    name = models.CharField(max_length=100)
    UniqueId = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name + " - " + self.description


class Observation(models.Model):
    name = models.CharField(max_length=100)
    UniqueId = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    pestTrap = models.ForeignKey(PestTrap, on_delete=models.CASCADE)
