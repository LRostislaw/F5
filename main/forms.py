from django import forms
from .models import AD, TypeData, puser, user_registrated
from django.forms import ModelForm, TextInput, CheckboxInput
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="email")
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput, help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label="Пароль (Повторно)", widget=forms.PasswordInput, help_text='Повторите пароль')

    def clean_password1(self):
        password1 = self.cleaned_data["password1"]
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError('Пароли не совпадают', code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registrated.send(RegisterUserForm, instance=user)
        return user

    choices = (('False', 'Пациент'), ('True', 'Врач'))
    is_doctor = forms.ChoiceField(choices=choices, widget=forms.Select(
        attrs={'class': 'auth_form_form,  col-md-9',
               'style': 'width: 238px; height: 25px; padding: 0; font-family: Roboto; font-style: normal; font-weight: 300; font-size: 14px; line-height: 14px; color: #FFFFFF; text-align: center; background: #008982; border-radius: 5px; border: none; display: block; margin: 0 auto; '
               }))

    class Meta:
        model = puser

        fields = ['username', 'email', 'password1', 'password2', 'send_messages', 'is_doctor']

        widgets = {
            'send_messages': CheckboxInput(attrs={
                'class': 'form-check-input col-md-1 auth_checkbox',
            }),
        }


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


class AddPatientForm(ModelForm):
    email = forms.EmailField(required=True, label="email", widget=forms.TextInput(attrs={
                'class': 'form-control ',
                'type': 'email',
                'style': 'margin: 0 auto; margin-top:5px; width:95%;',
                'placeholder': 'email пациента',
            }))

    class Meta:
        model = puser
        fields = ['email']