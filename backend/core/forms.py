from django import forms
from django.forms import ModelForm
from .models import PestTrap

# Create the form class.
class PestTrapForm(ModelForm):
    class Meta:
        model = PestTrap
        fields = ["name", "UniqueId", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "name_field"}),
            "UniqueId": forms.TextInput(attrs={"class": "UniqueId_field"}),
            "description": forms.TextInput(attrs={"class": "description_field"}),
        }
