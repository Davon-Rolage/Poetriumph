from string import ascii_letters, digits

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import ValidationError
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from .models import CustomUser
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')
        
    username = forms.CharField(required=True, max_length=15, widget=forms.TextInput(
        attrs={
            'class': 'form-control border-info placeicon',
            'placeholder': mark_safe('&#xf007; &nbsp; Username'),
            }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={
            'class': 'form-control border-info placeicon',
            'placeholder': mark_safe('&#xf0e0; &nbsp; Email'),
        }
    ))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control border-info placeicon',
            'placeholder': mark_safe('&#xf084; &nbsp; Enter password...'),
            }))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control border-info placeicon',
            'placeholder': mark_safe('&#xf084; &nbsp; Confirm password...'),
        }
    ))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    
    def clean(self):
        cleaned_data = super().clean()
        captcha = cleaned_data.get('captcha')
        if not captcha:
            self.add_error('captcha', ValidationError(_('You must pass the reCAPTCHA test')))
            return cleaned_data
        
        username = cleaned_data.get('username')
        username_allowed_chars = ascii_letters + digits + '@.+-_'
        email = cleaned_data.get('email')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        # Check if username contains invalid characters
        if username and not all(char in username_allowed_chars for char in username):
            if username and ' ' in username:
                self.add_error('username', ValidationError(_('Username cannot contain spaces')))
                self.fields['username'].widget.attrs.update({'class': 'form-control border-danger placeicon'})
            else:
                self.add_error('username', ValidationError(_('Username contains invalid characters')))
                self.fields['username'].widget.attrs.update({'class': 'form-control border-danger placeicon'})
            
        if username and len(username) < 3:
            self.add_error('username', ValidationError(_('Username is too short')))
            self.fields['username'].widget.attrs.update({'class': 'form-control border-danger placeicon'})
            
        if username and len(username) > 15:
            self.add_error('username', ValidationError(_('Username is too long')))
            self.fields['username'].widget.attrs.update({'class': 'form-control border-danger placeicon'})
        
        if email and '@' not in email:
            self.add_error('email', ValidationError(_('Email contains invalid characters')))
            self.fields['email'].widget.attrs.update({'class': 'form-control border-danger placeicon'})
            
        if password1 and len(password1) < 8:
            self.fields['password1'].widget.attrs.update({'class': 'form-control border-danger placeicon'})
            
        if password1 and password1 != password2:
            self.fields['password2'].widget.attrs.update({'class': 'form-control border-danger placeicon'})
        
        return cleaned_data


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('is_premium',)


class CustomUserLoginForm(forms.Form):
    class Meta:
        model = CustomUser
        fields = '__all__'
        
    username = forms.CharField(required=True, max_length=15, widget=forms.TextInput(
        attrs={
            'class': 'form-control border-info placeicon',
            'placeholder': mark_safe('&#xf007; &nbsp; Username'),
        }
    ))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control border-info placeicon',
            'placeholder': mark_safe('&#xf084; &nbsp; Enter password...'),
        }
    ))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    
    def clean(self):
        cleaned_data = super().clean()
        captcha = cleaned_data.get('captcha')
        if not captcha:
            self.add_error('captcha', ValidationError(_('You must pass the reCAPTCHA test')))
            return cleaned_data
        
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            self.add_error('username', ValidationError(_('Invalid username or password')))
        return cleaned_data
  