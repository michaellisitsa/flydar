from django import forms
from django.forms import ModelForm
from .models import PestTrap

# Create the Pest Trap form class.
class PestTrapForm(ModelForm):
    class Meta:
        model = PestTrap
        fields = ["name", "UniqueId", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "name_field"}),
            "UniqueId": forms.TextInput(attrs={"class": "UniqueId_field"}),
            "description": forms.TextInput(attrs={"class": "description_field"}),
        }


# Create the Observation form class.
class ObservationForm(ModelForm):
    pestTrap = forms.ModelChoiceField(queryset=PestTrap.objects.all())

    class Meta:
        model = PestTrap
        fields = ["name", "UniqueId", "description", "pestTrap"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "name_field"}),
            "UniqueId": forms.TextInput(attrs={"class": "UniqueId_field"}),
            "description": forms.TextInput(attrs={"class": "description_field"}),
        }
