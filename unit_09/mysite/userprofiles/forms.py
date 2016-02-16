# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    username = forms.RegexField(label="Username", max_length=30,
        regex=r'^[\w.-]+$', error_messages={'invalid': 'This value may contain only letters, numbers and ./-/_ characters.'})
    email = forms.EmailField(label='E-mail')
    password = forms.CharField(label='Password',
        widget=forms.PasswordInput(render_value=False))

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class' : 'form-control'})
        self.fields['username'].widget.attrs.update({'placeholder' : 'Enter Your User Name'})

        self.fields['email'].widget.attrs.update({'class' : 'form-control'})
        self.fields['email'].widget.attrs.update({'placeholder' : 'johndoe@company.com'})

        self.fields['password'].widget.attrs.update({'class' : 'form-control'})
        self.fields['password'].widget.attrs.update({'placeholder' : 'Easy to remember, hard to guess'})

    def save(self, *args, **kwargs):
        new_user = User.objects.create_user(
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password'],
                email=self.cleaned_data['email']
            )

        if hasattr(self, 'save_profile'):
            self.save_profile(new_user, *args, **kwargs)

        return new_user
