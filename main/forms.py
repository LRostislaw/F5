from .models import AD
from django.forms import ModelForm, TextInput, CharField


class ADForm(ModelForm):
    class Meta:
        model = AD
        fields = ['systolic_ad', 'diastolic_ad']

        widgets = {
            'systolic_ad': TextInput(attrs={
                'class': 'form-control save_form',
                'type': 'number',
                'placeholder': 'Систолическое давление',
            }),
            'diastolic_ad': TextInput(attrs={
                'class': 'form-control save_form',
                'type': 'number',
                'placeholder': 'Диастолическое давление',
            })
        }
