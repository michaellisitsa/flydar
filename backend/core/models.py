from django.db import models
from django.contrib.auth.models import User


class PestTrap(models.Model):
    """A model for pest traps."""
    
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.pk


class Observation(models.Model):
    """A model for the observations related to pest traps."""

    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    pestTrap = models.ForeignKey(PestTrap, on_delete=models.CASCADE)
