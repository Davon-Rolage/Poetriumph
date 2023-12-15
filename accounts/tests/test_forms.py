from unittest import mock

from django.contrib.auth import get_user_model
from django.test import TestCase, tag

from accounts.forms import CustomUserCreationForm, CustomUserLoginForm
from poetry_translation.config import GUI_MESSAGES


GUI_MESSAGES_FORMS = GUI_MESSAGES['forms']


@tag("accounts", "form", "form_custom_user_creation")
class CustomUserCreationFormTestCase(TestCase):
    
    def create_invalid_form(self, error_fields):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@localhost',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        for k, v in error_fields.items():
            form_data[k] = v

        return CustomUserCreationForm(data=form_data)
    
    @mock.patch("captcha.fields.ReCaptchaField.clean")
    def test_custom_user_creation_form_valid_data(self, mock_clean):
        mock_clean.return_value = "testcaptcha"
        form = CustomUserCreationForm(data={
            'username': 'testuser',
            'email': 'testuser@localhost',
            'password1': 'testpassword',
            'password2': 'testpassword',
        })
        self.assertTrue(form.is_valid())

    def test_custom_user_creation_form_invalid_captcha(self):
        form = CustomUserCreationForm(data={
            'username': 'testuser',
            'email': 'testuser@localhost',
            'password1': 'testpassword',
            'password2': 'testpassword',
        })
        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'captcha', GUI_MESSAGES_FORMS['error_captcha'])

    def test_custom_user_creation_form_invalid_username_empty(self):
        form = self.create_invalid_form({'username': ''})
        
        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'username', GUI_MESSAGES_FORMS['error_username_required'])

    def test_custom_user_creation_form_invalid_username_contains_spaces(self):
        form = self.create_invalid_form({'username': 'a b c'})
        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'username', GUI_MESSAGES_FORMS['error_username_contains_spaces'])

    def test_custom_user_creation_form_invalid_username_contains_invalid_chars(self):
        form = self.create_invalid_form({'username': 'user@name'})
        
        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'username', GUI_MESSAGES_FORMS['error_username_invalid_chars'])

    def test_custom_user_creation_form_invalid_username_too_short(self):
        form = self.create_invalid_form({'username': 'a'})
        
        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'username', GUI_MESSAGES_FORMS['error_username_min_length'])

    def test_custom_user_creation_form_invalid_username_too_long(self):
        form = self.create_invalid_form({'username': 'a' * 16})

        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'username', GUI_MESSAGES_FORMS['error_username_max_length'])

    def test_custom_user_creation_form_invalid_password_too_short(self):
        form = self.create_invalid_form({'password1': 'pass'})
        
        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'password1', GUI_MESSAGES_FORMS['error_password_min_length'])

    def test_custom_user_creation_form_invalid_passwords_do_not_match(self):
        form = self.create_invalid_form({'password2': 'mismatchedpassword'})
        
        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'password2', 'The two password fields didn’t match.')


@tag("accounts", "form", "form_custom_user_login")
class CustomUserLoginFormTestCase(TestCase):
    fixtures = ['test_users.json']
    
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.test_user = cls.User.objects.first()
    
    @mock.patch("captcha.fields.ReCaptchaField.clean")
    def test_custom_user_login_form_valid_data(self, mock_clean):
        mock_clean.return_value = "testcaptcha"
        form = CustomUserLoginForm(data={
            'username': 'test_user',
            'password': 'test_password',
        })
        self.assertTrue(form.is_valid())
    
    def test_custom_user_login_form_invalid_captcha(self):
        form = CustomUserLoginForm(data={
            'username': 'test_user',
            'password': 'test_password',
        })
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors['captcha'][0] == GUI_MESSAGES_FORMS['error_captcha'])
    
    def test_custom_user_login_form_invalid_captcha_invalid_username(self):
        form = CustomUserLoginForm(data={
            'username': 'user_invalid',
            'password': 'test_password',
        })
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors['captcha'][0] == GUI_MESSAGES_FORMS['error_captcha'])
        self.assertFormError(form, 'username', [])
    
    @mock.patch("captcha.fields.ReCaptchaField.clean")
    def test_custom_user_login_form_invalid_username(self, mock_clean):
        mock_clean.return_value = "testcaptcha"
        form = CustomUserLoginForm(data={
            'username': 'user_invalid',
            'password': 'test_password',
        })
        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'username', GUI_MESSAGES_FORMS['error_invalid_credentials'])

    @mock.patch("captcha.fields.ReCaptchaField.clean")
    def test_custom_user_login_form_invalid_password(self, mock_clean):
        mock_clean.return_value = 'testcaptcha'
        form = CustomUserLoginForm(data={
            'username': 'test_user',
            'password': 'password_invalid',
        })
        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'username', GUI_MESSAGES_FORMS['error_invalid_credentials'])
    