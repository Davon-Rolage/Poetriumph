from string import ascii_letters, digits

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.forms import ValidationError
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

from poetry_translation.config import GUI_MESSAGES

from .models import CustomUser


GUI_MESSAGES_FORMS = GUI_MESSAGES['forms']


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
        
    username = forms.CharField(max_length=15, widget=forms.TextInput(
        attrs={
            'class': 'form-control shadow-none',
            'id': 'floatingInputGroupUsername',
            }),
        error_messages={
            'required': GUI_MESSAGES_FORMS['error_username_required'],
            'invalid': GUI_MESSAGES_FORMS['error_username_invalid_chars'],
            'max_length': GUI_MESSAGES_FORMS['error_username_max_length'],
            'min_length': GUI_MESSAGES_FORMS['error_username_min_length'],
            'contains_spaces': GUI_MESSAGES_FORMS['error_username_contains_spaces'],
        }
    )
        
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control shadow-none',
            'id': 'floatingInputGroupEmail',
        }),
        error_messages={
            'invalid': GUI_MESSAGES_FORMS['error_email_invalid'],
        }
    )
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control shadow-none',
            'id': 'floatingInputGroupPassword1',
            }
        )
    )
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control shadow-none',
            'id': 'floatingInputGroupPassword2',
        }),
    )
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(),
        error_messages={
            'required': GUI_MESSAGES_FORMS['error_captcha'],
        })
    
    def clean(self):
        cleaned_data = super().clean()
        
        username_allowed_chars = ascii_letters + digits + '.+-_'
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        # Check if username contains invalid characters
        if username and not all(char in username_allowed_chars for char in username):
            if ' ' in username:
                self.add_error('username', ValidationError(GUI_MESSAGES_FORMS['error_username_contains_spaces']))
                self.fields['username'].widget.attrs.update({'class': 'form-control border-danger'})
            else:
                self.add_error('username', ValidationError(GUI_MESSAGES_FORMS['error_username_invalid_chars']))
                self.fields['username'].widget.attrs.update({'class': 'form-control border-danger'})
            
        if username and len(username) < 3:
            self.add_error('username', ValidationError(GUI_MESSAGES_FORMS['error_username_min_length']))
            self.fields['username'].widget.attrs.update({'class': 'form-control border-danger'})

        if password1 and len(password1) < 8:
            self.add_error('password1', ValidationError(GUI_MESSAGES_FORMS['error_password_min_length']))
            self.fields['password1'].widget.attrs.update({'class': 'form-control border-danger'})

        if password1 and password1 != password2:
            self.fields['password2'].widget.attrs.update({'class': 'form-control border-danger'})
        
        return cleaned_data

    def send_activation_email(self, request=None, user=None, user_token=None):
        mail_subject = GUI_MESSAGES['messages']['email_subject']
        to_email = self.cleaned_data.get('email')
        message = render_to_string('accounts/activate_email.html', {
            'username': user.username,
            'domain': get_current_site(request).domain,
            'token': user_token,
            'protocol': 'https' if request.is_secure() else 'http'
        })
        send_mail(mail_subject, message, html_message=message, from_email=None, recipient_list=[to_email])


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
            'class': 'form-control shadow-none',
            'id': 'floatingInputGroupUsername',
            'name': 'username',
        }
    ))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control shadow-none',
            'id': 'floatingInputGroupPassword',
            'name': 'password',
        }
    ))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(),
        error_messages={
            'required': GUI_MESSAGES_FORMS['error_captcha'],
        })
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        captcha = cleaned_data.get('captcha')
        
        if not captcha:
            self.add_error('captcha', ValidationError(GUI_MESSAGES_FORMS['error_captcha']))
            return cleaned_data

        user = authenticate(username=username, password=password)
        if not user:
            self.add_error('username', ValidationError(GUI_MESSAGES_FORMS['error_invalid_credentials']))
        return cleaned_data
  