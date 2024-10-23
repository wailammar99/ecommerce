from django import forms
from .models import *

class VegForm(forms.ModelForm):
    class Meta:
        model = Veg
        fields = ['name', 'price', 'img', 'existe']  