from django import forms
from django.forms import ModelForm
from .models import menu

class add_menu(ModelForm):
    class Meta:
        model=menu
        fields=('NAME','IMG','DESC','CUSINE','TYPE','NON_VEG','RATE','REST_ID')