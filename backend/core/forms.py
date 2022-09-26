from django import forms
from django.forms import ModelForm
from .models import Observation, PestTrap


class PestTrapForm(ModelForm):
    """A model form for registering pest traps."""
    class Meta:
        model = PestTrap
        fields = ["id", "name", "description"]
        widgets = {
            "id": forms.TextInput(attrs={"class": "UniqueId_field"}),
            "name": forms.TextInput(attrs={"class": "name_field"}),
            "description": forms.TextInput(attrs={"class": "description_field"}),
        }



class ObservationForm(ModelForm):
    """A model form for registering pest trap observations."""
    pestTrap = forms.ModelChoiceField(queryset=PestTrap.objects.all())

    class Meta:
        model = Observation 
        fields = ["id", "pestTrap", "name", "description"]
        widgets = {
            "id": forms.TextInput(attrs={"class": "UniqueId_field"}),
            "name": forms.TextInput(attrs={"class": "name_field"}),
            "description": forms.TextInput(attrs={"class": "description_field"})
        }
