from unittest import mock

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase, tag
from django.urls import reverse


@tag("accounts", "view", "view_index")
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


@tag("accounts", "view", "view_signup")
class SignupViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('signup')
        cls.template_name = 'accounts/signup.html'
    
    def test_signup_view_GET(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        self.assertIsNotNone(response.context['form'])
    
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
        self.assertIn('alert-success', response.content.decode('utf-8'))
    
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


@tag("accounts", "view", "view_login")
class LoginViewTestCase(TestCase):
    fixtures = ['test_users.json', 'test_profiles.json']
    
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.url = reverse('login')
        cls.template_name = 'accounts/login.html'
        cls.test_user = cls.User.objects.first()
        
    def test_login_view_GET(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        self.assertIsNotNone(response.context['form'])
    
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


@tag("accounts", "view", "view_logout")
class LogoutViewTestCase(TestCase):
    fixtures = ['test_users.json']
    
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.url = reverse('logout')
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


@tag("accounts", "view", "view_profile")
class ProfileViewTestCase(TestCase):
    fixtures = ['test_users.json', 'test_profiles.json']
    
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.url = reverse('profile')
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
        

@tag("accounts", "view", "view_delete_user")
class DeleteUserViewTestCase(TestCase):
    fixtures = ['test_users.json']
    
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()

        cls.test_user_to_be_deleted = cls.User.objects.create(
            username='test_user_to_be_deleted'
        )
        cls.url = reverse('delete_user', kwargs={'pk': cls.test_user_to_be_deleted.pk})
        cls.template_name_redirect = 'poetry_translation/index.html'
    
    def test_delete_user_view_as_logged_in_user(self):
        self.client.force_login(self.test_user_to_be_deleted)
        response = self.client.post(self.url, follow=True)
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed = self.template_name_redirect
        self.assertEqual(str(messages[0]), 'The user has been successfully deleted')
        self.assertFalse(self.User.objects.filter(pk=self.test_user_to_be_deleted.pk).exists())


@tag("accounts", "view", "view_premium")
class PremiumViewTestCase(TestCase):    
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('premium')
        cls.template_name = 'poetry_translation/premium.html'
    
    def test_premium_view_GET(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
    
    def test_premium_view_method_not_allowed_POST(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)


@tag("accounts", "view", "view_get_premium")
class GetPremiumViewTestCase(TestCase):
    fixtures = ['test_users.json', 'test_profiles.json']
    
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.url = reverse('get_premium')
        
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

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('premium'))
        self.assertTrue(self.test_user.is_premium)
    
    def test_get_premium_view_was_premium_POST(self):
        self.client.force_login(self.test_user_premium)
        response = self.client.post(self.url)
        
        self.test_user_premium.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('premium'))
        self.assertTrue(self.test_user_premium.is_premium)


@tag("accounts", "view", "view_cancel_premium")
class CancelPremiumViewTestCase(TestCase):
    fixtures = ['test_users.json', 'test_profiles.json']
    
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        
        cls.url = reverse('cancel_premium')
        cls.url_redirect = reverse('premium')
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
