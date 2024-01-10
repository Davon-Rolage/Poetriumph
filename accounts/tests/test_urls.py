from django.test import SimpleTestCase, tag
from django.urls import resolve, reverse

from accounts.views import *


@tag("url", "url_accounts")
class AccountsUrlsTestCase(SimpleTestCase):
    
    def test_signup_url_resolves(self):
        url = reverse('accounts:signup')
        self.assertEqual(resolve(url).func.view_class, SignUpView)
    
    def test_activate_user_url_resolves(self):
        url = reverse('accounts:activate_user', args=['token'])
        self.assertEqual(resolve(url).func.view_class, ActivateUserView)

    def test_login_url_resolves(self):
        url = reverse('accounts:login')
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_logout_url_resolves(self):
        url = reverse('accounts:logout')
        self.assertEqual(resolve(url).func, logout_view)

    def test_profile_url_resolves(self):
        url = reverse('accounts:profile')
        self.assertEqual(resolve(url).func.view_class, ProfileView)

    def test_deactivate_user_url_resolves(self):      
        url = reverse('accounts:deactivate_user')
        self.assertEqual(resolve(url).func.view_class, DeactivateUserView)

    def test_check_username_exists_url_resolves(self):
        url = reverse('accounts:check_username_exists')
        self.assertEqual(resolve(url).func, check_username_exists)

    def test_premium_url_resolves(self):
        url = reverse('accounts:premium')
        self.assertEqual(resolve(url).func.view_class, PremiumView)

    def test_get_premium_url_resolves(self):
        url = reverse('accounts:get_premium')
        self.assertEqual(resolve(url).func.view_class, GetPremiumView)

    def test_cancel_premium_url_resolves(self):
        url = reverse('accounts:cancel_premium')
        self.assertEqual(resolve(url).func.view_class, CancelPremiumView)
