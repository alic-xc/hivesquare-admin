from django import forms
from django.forms.widgets import TextInput


class LoginForm(forms.Form):
    username = forms.CharField(required=True, widget=TextInput(attrs={'class': 'form-control',
                                                                      'type': 'text', 'id': 'username',
                                                                      'placeholder': 'Username'
                                                                      }))
    password = forms.CharField(required=True, widget=TextInput(attrs={'class': 'form-control',
                                                                      'type': 'password', 'id': 'password',
                                                                      'placeholder': 'Password'
                                                                      }))


class BankForm(forms.Form):
    bank_name = forms.CharField(required=True, widget=TextInput(attrs={'class': ' form-control',
                                                                        'type': 'text', 'id': 'title',
                                                                        'placeholder': 'Enter Bank Name'}))
    bank_code = forms.CharField(required=False, widget=TextInput(attrs={'class': ' form-control',
                                                                        'type': 'text', 'id': 'title',
                                                                        'placeholder': 'Enter Bank Code'}))
