from django.contrib.auth import get_user_model
from django.test import TestCase, tag

from accounts.models import CustomUserToken, CustomUserTokenType


@tag("model", "model_custom_user")
class CustomUserModelTestCase(TestCase):
    fixtures = ['test_users.json']
    
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        
        test_users = cls.User.objects.all()
        cls.test_user = test_users.first()
        cls.test_user_staff = test_users.get(username='test_user_staff')
        cls.test_created_superuser = cls.User.objects.create_user(
            username='test_created_superuser',
            is_staff=True,
            is_superuser=True
        )
        cls.test_user_deactivated = test_users.get(
            username__icontains='test_user_deactivated'
        )
        cls.test_user_inactive = cls.User.objects.create_user(
            username='test_user_inactive'
        )
    
    def test_custom_user_str(self):
        self.assertEqual(str(self.test_user), 'test_user')
    
    def test_custom_user_deactivated_str(self):
        self.assertEqual(
            str(self.test_user_deactivated), 
            f'test_user_deactivated - ({self.test_user_deactivated.id})'
        )
    
    def test_custom_user_save_method_does_not_make_regular_user_active(self):
        self.assertFalse(self.test_user_inactive.is_active)
    
    def test_custom_user_save_method_makes_staff_user_active(self):
        self.assertTrue(self.test_user_staff.is_active)
    
    def test_custom_user_save_method_makes_superuser_active(self):
        self.assertTrue(self.test_created_superuser.is_active)
    
    def test_custom_user_user_profile_exists_when_user_is_active(self):
        self.assertTrue(self.test_user.profile)
    
    def test_custom_user_profile_exists_when_user_is_inactive(self):
        self.assertTrue(hasattr(self.test_user_inactive, 'profile'))


@tag("model", "model_profile")
class ProfileTestCase(TestCase):
    fixtures = ['test_users.json']
    
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.test_user = cls.User.objects.first()
        cls.test_user_profile = cls.test_user.profile
    
    def test_profile_str(self):
        self.assertEqual(str(self.test_user_profile), 'Profile test_user')


@tag("model", "model_custom_user_token")
class CustomUserTokenTestCase(TestCase):
    fixtures = ['test_users.json', 'token_types.json']
    
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.test_user = cls.User.objects.first()
        token_type = CustomUserTokenType.objects.first()
        cls.test_user_token = CustomUserToken.objects.create(
            user=cls.test_user, 
            token_type=token_type,
            token='test_token'
        )
        cls.token = cls.test_user_token.token
    
    def test_custom_user_token_str(self):
        self.assertEqual(str(self.test_user_token), 'test_user - test_token')


@tag("model", "model_custom_user_token_type")
class CustomUserTokenTypeTestCase(TestCase):
    fixtures = ['token_types.json']
    
    @classmethod
    def setUpTestData(cls):
        cls.token_type = CustomUserTokenType.objects.first()
    
    def test_custom_user_token_type_str(self):
        self.assertEqual(str(self.token_type), self.token_type.name)
    
    def test_custom_user_token_type_list_all(self):
        token_types = CustomUserTokenType.objects.all()
        self.assertEqual(len(token_types), 4)
        names = [tt.name for tt in token_types]
        self.assertEqual(names, ['User activation', 'Password reset', 'Username change', 'Email change'])
        