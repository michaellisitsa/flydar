"""
Creates initial grower and inspector groups.
Sets model permissions for both groups.
"""

import logging

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission


def assign_permissions(group, model_permissions):
    for key, value in model_permissions.items():
        for permission in value:
            name = f"Can {permission} {key}"
            print(f"Creating permission: {group} {name}")

            try:
                model_add_perm = Permission.objects.get(name=name)
            except Permission.DoesNotExist:
                logging.warning("Permission not found with name '{}'.".format(name))
                continue

            group.permissions.add(model_add_perm)


# Create initial inspector/grower groups and permissions
class Command(BaseCommand):
    help = "Create initial inspector/grower groups and permissions"

    def handle(self, *args, **options):
        inspector_group, _ = Group.objects.get_or_create(name="inspectors")
        assign_permissions(
            group=inspector_group,
            model_permissions={
                "pest trap": ["view", "add", "change", "delete"],
                "observation": ["view", "add", "change", "delete"],
            },
        )
        grower_group, _ = Group.objects.get_or_create(name="growers")
        assign_permissions(
            group=grower_group,
            model_permissions={
                "pest trap": ["view", "change"],
                "observation": ["view"],
            },
        )

        print("Created default groups and permissions.")
