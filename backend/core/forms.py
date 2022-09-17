from django import forms
from django.forms import ModelForm
from .models import PestTrap

# Create the form class.
class PestTrapForm(ModelForm):
    class Meta:
        model = PestTrap
        fields = ["name", "UniqueId", "description"]
