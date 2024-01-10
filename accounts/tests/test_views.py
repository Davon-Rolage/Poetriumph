import os
from unittest import mock, skipIf

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.messages import get_messages
from django.test import TestCase, tag
from django.urls import reverse

from accounts.models import *
from accounts.tokens import generate_user_token
from poetry_translation.gui_messages import GUI_MESSAGES


@tag("view", "view_index")
class IndexViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('translation')
    
    def test_index_view_GET(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_index_view_method_not_allowed_POST(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)


@tag("view", "view_signup")
class SignupViewTestCase(TestCase):
    fixtures = ['token_types.json']
    
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.url = reverse('accounts:signup')
        cls.template_name = 'accounts/signup.html'
    
    def test_signup_view_GET(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        self.assertIsNotNone(response.context['form'])
    
    @skipIf(not os.environ.get('WORKERS_RUNNING'), 'Celery workers not running')
    @mock.patch("captcha.fields.ReCaptchaField.clean")
    def test_signup_view_form_valid_POST(self, mock_clean):
        mock_clean.return_value = "testcaptcha"
        form_data = {
            'username': 'test_user',
            'email': 'test@example.com',
            'password1': 'test_password',
            'password2': 'test_password',
        }
        response = self.client.post(self.url, data=form_data, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'poetry_translation/index.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        success_message = GUI_MESSAGES['messages']['activation_email_sent'].format(
            user=form_data['username'], to_email=form_data['email']
        )
        self.assertEqual(str(messages[0]), success_message)
        user = self.User.objects.get(username=form_data['username'])
        self.assertFalse(user.is_active)
        self.assertTrue(hasattr(user, 'profile'))
    
    def test_signup_view_form_invalid_POST(self):
        form_data = {
            'username': 'test_user',
            'email': 'test@example.com',
            'password1': 'test_password',
            'password2': 'test_password',
        }
        response = self.client.post(self.url, data=form_data, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        self.assertIn('alert-danger', response.content.decode('utf-8'))
        self.assertIsNotNone(response.context['form'])


@tag("view", "view_login")
class LoginViewTestCase(TestCase):
    fixtures = ['test_users.json']
    
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.url = reverse('accounts:login')
        cls.template_name = 'accounts/login.html'
        cls.test_user = cls.User.objects.first()
        
    def test_login_view_GET(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        self.assertIsNotNone(response.context['form'])
    
    @mock.patch("captcha.fields.ReCaptchaField.clean")
    def test_redirects_to_next_url_after_login_GET_POST(self, mock_clean):
        from poetry_translation.models import Poem
        Poem.objects.create(saved_by=self.test_user)

        mock_clean.return_value = "testcaptcha"
        
        initial_url = '/en/poems/1/update/'
        redirects_to_url = f'{self.url}?next={initial_url}'
        form_data = {
            'username': 'test_user',
            'password': 'test_password',
            'next': initial_url
        }
        response = self.client.get(initial_url, follow=True)
        self.assertRedirects(response, redirects_to_url)
        
        response = self.client.post(redirects_to_url, data=form_data, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, initial_url)
        self.assertTemplateUsed(response, 'poetry_translation/poem_update.html')
        self.assertTemplateNotUsed(response, 'poetry_translation/index.html')
    
    @mock.patch("captcha.fields.ReCaptchaField.clean")
    def test_login_view_form_valid_POST(self, mock_clean):
        mock_clean.return_value = "testcaptcha"
        form_data = {
            'username': 'test_user',
            'password': 'test_password',
        }
        response = self.client.post(self.url, data=form_data, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'poetry_translation/index.html')
    
    @mock.patch("captcha.fields.ReCaptchaField.clean")
    def test_login_view_form_valid_stay_signed_in_POST(self, mock_clean):
        mock_clean.return_value = "testcaptcha"
        form_data = {
            'username': 'test_user',
            'password': 'test_password',
            'stay_signed_in': True,
        }
        response = self.client.post(self.url, data=form_data, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'poetry_translation/index.html')
        self.assertEqual(response.wsgi_request.session.get_expiry_age(), 60*60*24*14) # 14 days
    
    def test_login_view_form_invalid_POST(self):
        form_data = {
            'username': 'test_user',
            'password': 'test_password',
        }
        response = self.client.post(self.url, data=form_data, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        self.assertIn('alert-danger', response.content.decode('utf-8'))
        self.assertIsNotNone(response.context['form'])
    
    @mock.patch("captcha.fields.ReCaptchaField.clean")
    def test_login_view_form_valid_wrong_credentials_POST(self, mock_clean):
        mock_clean.return_value = "testcaptcha"
        form_data = {
            'username': 'test_user',
            'password': 'wrong_password',
        }
        response = self.client.post(self.url, data=form_data, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        self.assertIn('alert-danger', response.content.decode('utf-8'))
        self.assertIsNotNone(response.context['form'])
    

@tag("view", "view_logout")
class LogoutViewTestCase(TestCase):
    fixtures = ['test_users.json']
    
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.url = reverse('accounts:logout')
        cls.template_name = 'poetry_translation/index.html'
        cls.test_user = cls.User.objects.first()
        
    def test_logout_view_as_anonymous_user_GET(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('translation'))
        self.assertTemplateUsed(self.template_name)
    
    def test_logout_view_as_authenticated_user_GET(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('translation'))
        self.assertTemplateUsed(self.template_name)
        self.assertFalse(response.wsgi_request.user.is_authenticated)


@tag("view", "view_profile")
class ProfileViewTestCase(TestCase):
    fixtures = ['test_users.json']
    
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.url = reverse('accounts:profile')
        cls.template_name = 'accounts/profile.html'
        cls.test_user = cls.User.objects.first()
    
    def test_profile_view_method_not_allowed_POST(self):
        self.client.force_login(self.test_user)
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 405)
        self.assertTemplateNotUsed(self.template_name)
        
    def test_profile_view_as_anonymous_user_GET(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('accounts/login.html')
        self.assertTemplateNotUsed(self.template_name)

    def test_profile_view_as_authenticated_user_GET(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.template_name)
        self.assertIsNotNone(response.context['user_profile'])
        

@tag("view", "view_deactivate_user")
class DeactivateUserViewTestCase(TestCase):
    fixtures = ['test_users.json']
    
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.url = reverse('accounts:deactivate_user')
        cls.template_name_redirect = 'poetry_translation/index.html'

        cls.test_user_to_be_deactivated = cls.User.objects.create_user(
            username='test_user_to_be_deactivated',
            password='test_password',
            email='example@example.com',
            is_active=True,
        )
    
    def test_deactivate_user_view_as_logged_in_user(self):
        login = self.client.login(username='test_user_to_be_deactivated', password='test_password')
        response = self.client.post(self.url, follow=True)

        self.assertTrue(login)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed = self.template_name_redirect

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), GUI_MESSAGES['messages']['user_deactivated'])
        user_id = self.test_user_to_be_deactivated.id
        deactivated_user = self.User.objects.get(pk=user_id)
        self.assertTrue(deactivated_user)
        self.assertFalse(deactivated_user.is_active)
        self.assertEqual(deactivated_user.email, '')
        self.assertEqual(deactivated_user.username, f'test_user_to_be_deactivated - deactivated {user_id}')


@tag("view", "view_premium")
class PremiumViewTestCase(TestCase):    
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('accounts:premium')
        cls.template_name = 'poetry_translation/premium.html'
    
    def test_premium_view_GET(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
    
    def test_premium_view_method_not_allowed_POST(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)


@tag("view", "view_get_premium")
class GetPremiumViewTestCase(TestCase):
    fixtures = ['test_users.json']
    
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.url = reverse('accounts:get_premium')
        cls.template_name = 'poetry_translation/premium.html'
        
        cls.test_user = cls.User.objects.first()
        cls.test_user_premium = cls.User.objects.get(username='test_user_premium')
    
    def test_get_premium_view_method_not_allowed_GET(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_get_premium_view_was_not_premium_POST(self):
        self.client.force_login(self.test_user)
        response = self.client.post(self.url)
        
        self.test_user.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.template_name)
        self.assertTrue(self.test_user.is_premium)
    
    def test_get_premium_view_was_premium_POST(self):
        self.client.force_login(self.test_user_premium)
        response = self.client.post(self.url)
        
        self.test_user_premium.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.template_name)
        self.assertTrue(self.test_user_premium.is_premium)


@tag("view", "view_cancel_premium")
class CancelPremiumViewTestCase(TestCase):
    fixtures = ['test_users.json']
    
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        
        cls.url = reverse('accounts:cancel_premium')
        cls.url_redirect = reverse('accounts:premium')
        cls.template_name_redirect = 'poetry_translation/premium.html'
        
        cls.test_user = cls.User.objects.first()
        cls.test_user_premium = cls.User.objects.get(username='test_user_premium')
        
    def test_cancel_premium_view_method_not_allowed_GET(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
    
    def test_cancel_premium_view_as_anonymous_user_POST(self):
        response = self.client.post(self.url, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.url_redirect)
        self.assertTemplateUsed(response, self.template_name_redirect)
    
    def test_cancel_premium_view_as_not_premium_user_POST(self):
        self.client.force_login(self.test_user)
        response = self.client.post(self.url, follow=True)
        
        self.test_user.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.url_redirect)
        self.assertFalse(self.test_user.is_premium)
        self.assertTemplateUsed(response, self.template_name_redirect)
    
    def test_cancel_premium_view_as_premium_user_POST(self):
        self.client.force_login(self.test_user_premium)
        response = self.client.post(self.url, follow=True)
        
        self.test_user_premium.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.url_redirect)
        self.assertFalse(self.test_user_premium.is_premium)
        self.assertTemplateUsed(response, self.template_name_redirect)


@tag('view', 'view_password_reset')
class PasswordResetViewTestCase(TestCase):
    fixtures = ['test_users.json', 'token_types.json']
    
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('accounts:password_reset')
        cls.template_name = 'accounts/password_forgot.html'
        cls.template_name_redirect = 'poetry_translation/index.html'
        
    def test_password_reset_view_GET(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
    
    @skipIf(not os.environ.get('WORKERS_RUNNING'), 'Celery workers not running')
    def test_password_reset_view_form_valid_POST(self):
        form_data = {
            'email': 'test6@example.com',
        }
        response = self.client.post(self.url, data=form_data, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name_redirect)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        success_message = GUI_MESSAGES['messages']['password_reset_email_sent'].format(
            to_email=form_data['email']
        )
        self.assertEqual(str(messages[0]), success_message)


@tag('view', 'view_password_reset_check')
class PasswordResetCheckViewTestCase(TestCase):
    fixtures = ['test_users.json', 'token_types.json']
    
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.template_name_redirect_success = 'accounts/password_set.html'
        cls.template_name_redirect_fail = 'accounts/login.html'
        cls.token_generator = PasswordResetTokenGenerator()
        
        cls.test_user_poet = cls.User.objects.get(username='test_user_poet')
        token_type = CustomUserTokenType.objects.get(name='Password reset')
        token = cls.token_generator.make_token(cls.test_user_poet)

        cls.test_token = CustomUserToken.objects.create(
            user=cls.test_user_poet,
            token_type=token_type,
            token=token,
        )
        cls.invalid_token = CustomUserToken.objects.create(
            user=cls.User.objects.create_user(username='temp', password='temp'),
            token_type=token_type,
            token=generate_user_token(cls.test_user_poet.id),
        )
        
    def test_password_reset_check_view_success_GET(self):
        url = reverse('accounts:password_reset_check', args=[self.test_token.token])
        response = self.client.get(url, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name_redirect_success)
    
    def test_password_reset_check_view_token_doesnt_exist_GET(self):
        url = reverse('accounts:password_reset_check', args=[self.test_token.token+'fail'])
        response = self.client.get(url, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name_redirect_fail)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), GUI_MESSAGES['error_messages']['password_reset_failed'])

    def test_password_reset_check_view_token_invalid_GET(self):
        url = reverse('accounts:password_reset_check', args=[self.invalid_token.token])
        response = self.client.get(url, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name_redirect_fail)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), GUI_MESSAGES['error_messages']['password_reset_failed'])
        with self.assertRaises(CustomUserToken.DoesNotExist):
            self.invalid_token.refresh_from_db()


@tag('view', 'view_set_password')
class SetPasswordViewTestCase(TestCase):
    fixtures = ['test_users.json', 'token_types.json']
    
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.template_name = 'accounts/password_set.html'
        cls.template_name_redirect = 'accounts/login.html'
        cls.token_generator = PasswordResetTokenGenerator()

        cls.test_user_poet = cls.User.objects.get(username='test_user_poet')
        token_type = CustomUserTokenType.objects.get(name='Password reset')
        token = cls.token_generator.make_token(cls.test_user_poet)

        cls.test_token = CustomUserToken.objects.create(
            user=cls.test_user_poet,
            token_type=token_type,
            token=token,
        )
    
    def test_set_password_view_GET(self):
        url = reverse('accounts:set_password', args=[self.test_token.token])
        response = self.client.get(url, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)

    def test_set_password_view_form_valid_POST(self):
        url = reverse('accounts:set_password', args=[self.test_token.token])
        form_data = {
            'password1': 'new_password',
            'password2': 'new_password',
        }
        response = self.client.post(url, data=form_data, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name_redirect)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), GUI_MESSAGES['messages']['password_reset_successful'])

        login_password_old = self.client.login(username='test_user_poet', password='test_password')
        self.assertFalse(login_password_old)
        self.client.logout()
        login_password_new = self.client.login(username='test_user_poet', password='new_password')
        self.assertTrue(login_password_new)

        with self.assertRaises(CustomUserToken.DoesNotExist):
            self.test_token.refresh_from_db()
        