from django.contrib import admin
from .models import PestTrap, Observation

# Registers models for the admin portal
admin.site.register(PestTrap)
admin.site.register(Observation)