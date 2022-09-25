"""
Create permission groups
Create permissions (read only) to models for a set of groups
"""

import logging

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

GROUPS = ['inspectors', 'growers']
MODELS = ['pest trap', 'observation']
PERMISSIONS = ['view', 'add', 'change', 'delete']  # For now only view permission by default for all, others include add, delete, change

# Create initial inspector/grower groups and permissions
class Command(BaseCommand):
    help = 'Create initial inspector/grower groups and permissions'

    def handle(self, *args, **options):
        for group in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group)
            for model in MODELS:
                for permission in PERMISSIONS:
                    name = f"Can {permission} {model}"
                    print(f"Creating permission: {new_group} {name}")

                    try:
                        model_add_perm = Permission.objects.get(name=name)
                    except Permission.DoesNotExist:
                        logging.warning("Permission not found with name '{}'.".format(name))
                        continue

                    new_group.permissions.add(model_add_perm)

        print("Created default groups and permissions.")