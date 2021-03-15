from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Notice
from django.utils.translation import gettext_lazy as _


class LoginUserForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class NoticeForm(ModelForm):
    class Meta:
        model = Notice
        fields = '__all__'
        # fields = ['title', 'description', 'production_year', 'mileage',
        #           'cubic_capacity', 'horse_power', 'fuel_type', 'picture',
        #           'date_published']  # user, date_added, is deleted
        widgets = {
            # 'date_published': forms.TextInput(attrs={'type': 'date'}),
            'title': forms.Textarea(attrs={'rows': 1, 'class':'form-group'}),
            'description': forms.Textarea(attrs={'rows': 5}),
            'date_published': forms.DateInput(format='%m%d%y',
                                              attrs={'class': 'form-control', 'placeholder': 'Select a date',
                                                     'type': 'date'}),
            'author': forms.HiddenInput(),
            'date_added': forms.HiddenInput(),
            'is_deleted': forms.HiddenInput()
        }
        labels = {
            'title': _('Tytuł'),
            'description': _('Opis'),
            'production_year': _('Rok produkcji'),
            'mileage': _('Przebieg'),
            'cubic_capacity': _('Pojemność'),
            'horse_power': _('Moc'),
            'fuel_type': _('Rodzaj paliwa'),
            'picture': _('Zdjęcie'),
            'currently': _('Obecne'),
            'date_published': _('Data publikacji'),
            'is_publicated': _('Czy opublikowany?'),
        }

        # fields = ['title', 'description', 'production_year', 'mileage',
        #           'cubic_capacity', 'horse_power', 'fuel_type', 'picture',
        #           'date_published']  # user, date_added, is deleted
