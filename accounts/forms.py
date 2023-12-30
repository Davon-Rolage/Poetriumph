from string import ascii_letters, digits

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ValidationError
from django.utils.translation import gettext as _

from poetry_translation.config import GUI_MESSAGES

from .tasks import *


GUI_MESSAGES_FORMS = GUI_MESSAGES['forms']
ERROR_FIELD_CLASS = 'form-control border-danger shadow-none'


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
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
                self.fields['username'].widget.attrs.update({'class': ERROR_FIELD_CLASS})
            else:
                self.add_error('username', ValidationError(GUI_MESSAGES_FORMS['error_username_invalid_chars']))
                self.fields['username'].widget.attrs.update({'class': ERROR_FIELD_CLASS})
            
        if username and len(username) < 3:
            self.add_error('username', ValidationError(GUI_MESSAGES_FORMS['error_username_min_length']))
            self.fields['username'].widget.attrs.update({'class': ERROR_FIELD_CLASS})

        if password1 and len(password1) < 8:
            self.add_error('password1', ValidationError(GUI_MESSAGES_FORMS['error_password_min_length']))
            self.fields['password1'].widget.attrs.update({'class': ERROR_FIELD_CLASS})

        if password1 and password1 != password2:
            self.fields['password2'].widget.attrs.update({'class': ERROR_FIELD_CLASS})

        email_exists = get_user_model().objects.filter(email=email).exists()
        if email_exists:
            self.add_error('email', ValidationError(GUI_MESSAGES_FORMS['error_email_already_exists']))
            self.fields['email'].widget.attrs.update({'class': ERROR_FIELD_CLASS})
        
        return cleaned_data

    def send_activation_email(self, user_id=None, domain=None, protocol=None, to_email=None, language=None):
        send_activation_email_task.delay(
            user_id=user_id, 
            domain=domain, 
            protocol=protocol, 
            to_email=to_email,
            language=language
        )


class PasswordResetForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control shadow-none',
            'id': 'floatingInputGroupEmail',
        }),
        error_messages={
            'invalid': GUI_MESSAGES_FORMS['error_email_invalid'],
        }
    )
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if email:
            email_exists = get_user_model().objects.filter(email=email).exists()
            if not email_exists:
                self.add_error('email', ValidationError(GUI_MESSAGES_FORMS['error_email_doesnt_exist']))
                self.fields['email'].widget.attrs.update({'class': ERROR_FIELD_CLASS})
        return cleaned_data

    def send_password_reset_email(self, user_id=None, domain=None, protocol=None, to_email=None, language=None):
        send_password_reset_email_task.delay(
            user_id=user_id,
            domain=domain, 
            protocol=protocol, 
            to_email=to_email,
            language=language
        )


class SetPasswordForm(forms.Form):
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
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and len(password1) < 8:
            self.add_error('password1', ValidationError(GUI_MESSAGES_FORMS['error_password_min_length']))
            self.fields['password1'].widget.attrs.update({'class': ERROR_FIELD_CLASS})

        if password1 and password1 != password2:
            self.add_error('password2', ValidationError(GUI_MESSAGES_FORMS['error_password_mismatch']))
            self.fields['password2'].widget.attrs.update({'class': ERROR_FIELD_CLASS})

        return cleaned_data


class CustomUserLoginForm(forms.Form):
    class Meta:
        model = get_user_model()
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
    stay_signed_in = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={
            'class': 'form-check-input shadow-none',
            'id': 'stay-signed-in',
            'type': 'checkbox',
        }
    ))
    
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
  