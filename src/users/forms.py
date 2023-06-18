from django import forms
from django.contrib.auth.models import User

from datetime import date
from calendar import monthrange
from users.models import UserExtension

MONTHS = [
    (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'),
    (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'),
    (9, 'Septiembre'),  (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')
]


class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=255, min_length=8, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=255,  widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=255,  widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    day = forms.IntegerField(
                            max_value=31,
                            min_value=1,
                            initial=date.today().day,
                            widget=forms.Select(
                                choices=[
                                    (day,day) for day in range(1, 31)
                                ],
                                attrs={'class': 'form-select'}
                            )
                        )
    month = forms.IntegerField(
                            max_value=12,
                            min_value=1,
                            initial=MONTHS[date.today().month - 1],
                            widget=forms.Select(choices=MONTHS, attrs={'class': 'form-select'})
                        )
    year = forms.IntegerField(
                            min_value=1900,
                            max_value=date.today().year,
                            initial=date.today().year,
                            widget=forms.Select(
                                    choices=[
                                        (year, year) for year in range(1900, date.today().year + 1)
                                    ],
                                    attrs={'class': 'form-select'}
                                )
                            )
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    verify_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


    def clean_verify_password(self):
        password = self.cleaned_data['password']
        v_password = self.cleaned_data['verify_password']

        if password != v_password:
            raise forms.ValidationError('Passwords must match')

        return v_password


    def clean_year(self):
        day = int(self.cleaned_data['day'])
        month = int(self.cleaned_data['month'])
        year = int(self.cleaned_data['year'])

        _, max_days = monthrange(year, month)


        if day > max_days:
            raise forms.ValidationError('Not valid Date')

        return year


class ProfileEditForm(forms.Form):
    username = forms.CharField(disabled=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(disabled=True, widget=forms.EmailInput(attrs={'class':'form-control'}))


    day = forms.IntegerField(
                            max_value=31,
                            min_value=1,
                            initial=date.today().day,
                            widget=forms.Select(
                                choices=[
                                    (day,day) for day in range(1, 31)
                                ],
                                attrs={'class':'form-select'}
                            )
                        )
    month = forms.IntegerField(
                            max_value=12,
                            min_value=1,
                            initial=MONTHS[date.today().month - 1],
                            widget=forms.Select(choices=MONTHS, attrs={'class': 'form-select'})
                        )
    year = forms.IntegerField(
                            min_value=1900,
                            max_value=date.today().year,
                            initial=date.today().year,
                            widget=forms.Select(
                                    choices=[
                                        (year, year) for year in range(1900, date.today().year + 1)
                                    ],
                                    attrs={'class':'form-select'}
                                )
                            )
    
    def clean_year(self):
        day = int(self.cleaned_data['day'])
        month = int(self.cleaned_data['month'])
        year = int(self.cleaned_data['year'])

        _, max_days = monthrange(year, month)

        if day > max_days:
            raise forms.ValidationError('Not Valid date')

        return year
        

    