from django import forms

from .models import AD, TypeData
from django.forms import ModelForm, TextInput, RadioSelect, ModelChoiceField, ChoiceField
from django.contrib.auth.models import AbstractUser


class ADForm(ModelForm):
    class Meta:
        model = AD

        widgets = {
            'systolic_ad': TextInput(attrs={
                'class': 'form-control save_form',
                'type': 'number',
                'style': 'margin: 0 auto; margin-top:5px; width:95%;',
                'placeholder': 'Систолическое давление',
            }),
            'diastolic_ad': TextInput(attrs={
                'class': 'form-control save_form',
                'type': 'number',
                'style': 'margin: 0 auto; margin-top:5px; width:95%;',
                'placeholder': 'Диастолическое давление',
            }),
            'time': TextInput(attrs={
                'class': 'form-control save_form',
                'style': 'margin: 0 auto; margin-top:5px; width:95%;',
                'type': 'date',
            }),
        }
        fields = ['systolic_ad', 'diastolic_ad', 'time']


class TypeForm(ModelForm):
    choices = (('AD', 'Артериальное давление'), ('SU', 'Сахар'))
    label = forms.ChoiceField(choices=choices, widget=forms.Select(attrs={'class': 'form-select', 'style': 'margin: 0 auto; margin-top:5px; width:95%;'}))

    class Meta:
        model = TypeData
        fields = ['label']


class ChangeUserInfoForm(ModelForm):
    class Meta:
        model = AbstractUser
        fields = ['username']
