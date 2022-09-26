from django import forms
from django.forms import ModelForm
from .models import PestTrap


class PestTrapForm(ModelForm):
    """A model form for registering pest traps."""
    class Meta:
        model = PestTrap
        fields = ["name", "UniqueId", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "name_field"}),
            "UniqueId": forms.TextInput(attrs={"class": "UniqueId_field"}),
            "description": forms.TextInput(attrs={"class": "description_field"}),
        }



class ObservationForm(ModelForm):
    """A model form for registering pest trap observations."""
    pestTrap = forms.ModelChoiceField(queryset=PestTrap.objects.all())

    class Meta:
        model = PestTrap
        fields = ["name", "UniqueId", "description", "pestTrap"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "name_field"}),
            "UniqueId": forms.TextInput(attrs={"class": "UniqueId_field"}),
            "description": forms.TextInput(attrs={"class": "description_field"}),
        }
