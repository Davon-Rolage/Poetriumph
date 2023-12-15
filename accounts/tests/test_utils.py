from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.core import mail
from django.test import TestCase, tag
from django.urls import reverse
from django.utils import timezone

from accounts.models import CustomUserToken


@tag("accounts", "utils", "utils_check_username_exists")
class CheckUsernameExistsTestCase(TestCase):
    fixtures = ['test_users.json']
    
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.url = reverse('check_username_exists')
        cls.request_data = {'username': 'test_user'}
        cls.test_user = cls.User.objects.first()
    
    def test_check_username_exists_method_not_allowed_POST(self):
        response = self.client.post(self.url, self.request_data)
        self.assertEqual(response.status_code, 405)
    
    def test_check_username_exists_username_available_GET(self):
        response = self.client.get(self.url, {'username': 'available_username'})
        self.assertEqual(response.status_code, 200)

    def test_check_username_exists_username_taken_GET(self):
        response = self.client.get(self.url, self.request_data)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'exists': True})
    
    def test_check_username_exists_username_empty_GET(self):
        response = self.client.get(self.url, {'username': ''})
        self.assertEqual(response.status_code, 204)


@tag("accounts", "utils", "utils_activate_user")
class ActivateUserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        
        cls.test_user_act_success = cls.User.objects.create_user(
            username='test_user_activation_success', password='test_password'
        )
        cls.test_user_invalid = cls.User.objects.create_user(
            username='test_user_invalid', password='test_password'
        )
        cls.test_user_expired = cls.User.objects.create_user(
            username='test_user_expired', password='test_password'
        )
        cls.test_token_success = CustomUserToken.objects.create(
            user=cls.test_user_act_success, token='test_token'
        ).token
        CustomUserToken.objects.create(user=cls.test_user_invalid, token='test_token_invalid')

        expire_date = timezone.now() - timezone.timedelta(days=30)
        CustomUserToken.objects.create(
            user=cls.test_user_expired, token='test_token_expired', expire_date=expire_date
        )
    
    def test_activate_user_method_not_allowed_POST(self):
        url = reverse('activate_user', args=['foo'])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, 405)
        
    def test_activate_user_success_GET(self):        
        url = reverse('activate_user', args=[self.test_token_success])
        response = self.client.get(url)
        
        self.test_user_act_success.refresh_from_db()
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(self.test_user_act_success.is_active, True)
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Thank you for confirming your email. You can now sign in to your account.')
        
        login = self.client.login(username='test_user_activation_success', password='test_password')
        self.assertTrue(login)
        
    def test_activate_user_failed_invalid_token_GET(self):
        url = reverse('activate_user', args=['test_invalid_token'])
        response = self.client.get(url)
        
        self.test_user_invalid.refresh_from_db()
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('signup'))
        self.assertFalse(self.test_user_invalid.is_active)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Activation link is invalid! Please try again.')
        
        login = self.client.login(username='test_user_invalid', password='test_password')
        self.assertFalse(login)
    
    def test_activate_user_failed_expired_token_GET(self):
        url = reverse('activate_user', args=['test_token_expired'])
        response = self.client.get(url)
        
        self.test_user_expired.refresh_from_db()
        
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.test_user_expired.is_active)
        self.assertFalse(CustomUserToken.objects.filter(token='test_token_expired').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Activation link is invalid! Please try again.')
        
        login = self.client.login(username='test_user_expired', password='test_password')
        self.assertFalse(login)
