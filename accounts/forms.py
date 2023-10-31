from string import ascii_letters, digits

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import ValidationError
from django.utils.translation import gettext as _

from poetry_translation.config import GUI_MESSAGES

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')
        
    username = forms.CharField(required=True, max_length=15, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'floatingInputGroupUsername',
            }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'id': 'floatingInputGroupEmail',
        }
    ))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'id': 'floatingInputGroupPassword1',
            }))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'id': 'floatingInputGroupPassword2',
        }
    ))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    
    def clean(self):
        cleaned_data = super().clean()
        captcha = cleaned_data.get('captcha')
        if not captcha:
            self.add_error('captcha', ValidationError(GUI_MESSAGES['forms']['error_captcha']))
            return cleaned_data
        
        username = cleaned_data.get('username')
        username_allowed_chars = ascii_letters + digits + '.+-_'
        email = cleaned_data.get('email')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        # Check if username contains invalid characters
        if username and not all(char in username_allowed_chars for char in username):
            if username and ' ' in username:
                self.add_error('username', ValidationError(GUI_MESSAGES['forms']['error_username_contains_spaces']))
                self.fields['username'].widget.attrs.update({'class': 'form-control border-danger placeicon'})
            else:
                self.add_error('username', ValidationError(GUI_MESSAGES['forms']['error_username_contains_invalid_chars']))
                self.fields['username'].widget.attrs.update({'class': 'form-control border-danger placeicon'})
            
        if username and len(username) < 3:
            self.add_error('username', ValidationError(GUI_MESSAGES['forms']['error_username_too_short']))
            self.fields['username'].widget.attrs.update({'class': 'form-control border-danger placeicon'})
            
        if username and len(username) > 15:
            self.add_error('username', ValidationError(GUI_MESSAGES['forms']['error_username_too_long']))
            self.fields['username'].widget.attrs.update({'class': 'form-control border-danger placeicon'})
        
        if email and '@' not in email:
            self.add_error('email', ValidationError(GUI_MESSAGES['forms']['error_invalid_email']))
            self.fields['email'].widget.attrs.update({'class': 'form-control border-danger placeicon'})
            
        if password1 and len(password1) < 8:
            self.add_error('password1', ValidationError(GUI_MESSAGES['forms']['error_password_too_short']))
            self.fields['password1'].widget.attrs.update({'class': 'form-control border-danger placeicon'})
            
        if password1 and password1 != password2:
            self.add_error('password2', ValidationError(GUI_MESSAGES['forms']['error_passwords_do_not_match']))
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
            'class': 'form-control',
            'id': 'floatingInputGroupUsername',
        }
    ))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'id': 'floatingInputGroupPassword',
        }
    ))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    
    def clean(self):
        cleaned_data = super().clean()
        captcha = cleaned_data.get('captcha')
        if not captcha:
            self.add_error('captcha', ValidationError(GUI_MESSAGES['forms']['error_captcha']))
            return cleaned_data
        
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            self.add_error('username', ValidationError(GUI_MESSAGES['forms']['error_invalid_credentials']))
        return cleaned_data
  