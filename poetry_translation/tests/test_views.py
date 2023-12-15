from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase, tag
from django.urls import reverse

from poetry_translation.config import *
from poetry_translation.views import *
from django.contrib.messages import get_messages


@tag('views', 'views_poetry', 'views_poetry_index')
class IndexViewTestCase(TestCase):
    fixtures = ['test_users.json']
    
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.url = reverse('translation')
        cls.template_name = 'poetry_translation/index.html'
        cls.test_user = cls.User.objects.first()
        cls.test_user_premium = cls.User.objects.get(username='test_user_premium')

    def test_index_view_as_anonymous_user_GET(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(response.context['character_limit'], CHARACTER_LIMIT)
        self.assertEqual(len(response.context['language_engines']), len(LANGUAGE_ENGINES))
        self.assertEqual(len(response.context['source_languages']), len(SUPPORTED_LANGUAGES))
        self.assertEqual(len(response.context['target_languages']), 3)

    def test_index_view_as_authenticated_user_GET(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(response.context['character_limit'], CHARACTER_LIMIT)
        self.assertEqual(len(response.context['language_engines']), len(LANGUAGE_ENGINES))
        self.assertEqual(len(response.context['source_languages']), len(SUPPORTED_LANGUAGES))
        self.assertEqual(len(response.context['target_languages']), 3)
    
    def test_index_view_as_premium_user_GET(self):
        self.client.force_login(self.test_user_premium)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(response.context['character_limit'], CHARACTER_LIMIT_PREMIUM)
        self.assertEqual(len(response.context['language_engines']), len(LANGUAGE_ENGINES))
        self.assertEqual(len(response.context['source_languages']), len(SUPPORTED_LANGUAGES))
        self.assertEqual(len(response.context['target_languages']), len(SUPPORTED_LANGUAGES[1:]))
    
    def test_index_view_method_not_allowed_POST(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)


@tag('views', 'views_poetry_get_translation')
class GetTranslationViewTestCase(TestCase):
    fixtures = ['test_users.json']
    
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.factory = RequestFactory()
        cls.url = reverse('get_translation')
        cls.test_user = cls.User.objects.first()
        cls.test_user_premium = cls.User.objects.get(username='test_user_premium')
        cls.request_data = {
            'language_engine': 'GoogleTranslator',
            'source_lang': 'english',
            'target_lang': 'spanish',
            'original_text': 'Hello'
        }

    def test_get_translation_as_anonymous_user_POST(self):
        request = self.factory.post(self.url, self.request_data)
        request.user = AnonymousUser()

        response = GetTranslation.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'success': True,
            'translation': 'Hola'
        })
        
    def test_get_translation_as_authenticated_user_POST(self):
        request = self.factory.post(self.url, self.request_data)
        request.user = self.test_user

        response = GetTranslation.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'success': True,
            'translation': 'Hola'
        })
    
    def test_get_translation_as_premium_user_POST(self):
        request = self.factory.post(self.url, self.request_data)
        request.user = self.test_user_premium

        response = GetTranslation.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'success': True,
            'translation': 'Hola'
        })


    def test_get_translation_method_not_allowed_GET(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
    

@tag('views', 'views_poetry_save_translation')
class SaveTranslationViewTestCase(TestCase):
    fixtures = ['test_users.json', 'test_profiles.json']
    
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.url = reverse('save_translation')
        cls.template_name = 'poetry_translation/poem_update.html'
        cls.test_user_staff = cls.User.objects.get(username='test_user_staff')
        cls.request_data = {
            'original_text': 'Hello',
            'translation': 'Hola',
            'source_lang': 'english',
            'target_lang': 'spanish',
            'language_engine': 'GoogleTranslator'
        }

    def test_save_translation_view_method_not_allowed_GET(self):
        self.client.force_login(self.test_user_staff)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
    
    def test_save_translation_view_as_anonymous_user_POST(self):
        response = self.client.post(self.url, self.request_data, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
    
    def test_save_translation_view_as_authenticated_user_POST(self):
        self.client.force_login(self.test_user_staff)
        response = self.client.post(self.url, self.request_data)
        
        poem_test_user_staff = Poem.objects.get(saved_by=self.test_user_staff)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('poem_update', kwargs={'pk': poem_test_user_staff.pk}))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), GUI_MESSAGES['messages']['badge_earned'])
        
        
@tag('views', 'views_poetry_poem_detail')
class PoemDetailViewTestCase(TestCase):
    fixtures = ['test_users.json', 'test_poems.json']
    
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.url = reverse('poem_detail', args=[1])
        cls.template_name = 'poetry_translation/poem_detail.html'
        cls.test_user = cls.User.objects.first()
    
    def test_poem_detail_view_as_anonymous_user_GET(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        self.assertNotContains(response, 'id="btn-change-poem"')
    
    def test_poem_detail_view_as_authenticated_user_GET(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        self.assertContains(response, 'id="btn-change-poem"')
    
    def test_poem_detail_view_method_not_allowed_POST(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)


@tag('views', 'views_poetry_poem_update')
class PoemUpdateViewTestCase(TestCase):
    fixtures = ['test_users.json', 'test_poems.json']
    
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.test_user = cls.User.objects.first()
        cls.test_poem = Poem.objects.get(pk=1)
        cls.url = reverse('poem_update', kwargs={'pk': cls.test_poem.pk})
    
    def test_poem_update_view_as_anonymous_user_GET(self):
        response = self.client.get(self.url, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('login') + '?next=' + self.url)
        self.assertTemplateUsed(response, 'accounts/login.html')
    
    def test_poem_update_view_get_context_data(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'poetry_translation/poem_update.html')
        self.assertIn('gui_messages', response.context)
    
    def test_poem_update_form_valid(self):
        self.client.force_login(self.test_user)
        form_data = {
            'id': 1,
            'title': 'new_title',
            'original_text': 'new_original_text',
            'translation': 'new_translation',
            'source_lang': 'russian',
            'target_lang': 'french',
            'language_engine': 'ChatGptTranslator',
            'updated_at': '2022-01-01'
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('poem_detail', kwargs={'pk': 1}))
        self.test_poem.refresh_from_db()
        self.assertEqual(self.test_poem.title, 'new_title')
        self.assertEqual(self.test_poem.original_text, 'new_original_text')
        self.assertEqual(self.test_poem.translation, 'new_translation')
        self.assertEqual(self.test_poem.source_lang, 'russian')
        self.assertEqual(self.test_poem.target_lang, 'french')
        self.assertEqual(self.test_poem.language_engine, 'ChatGptTranslator')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'The poem has been successfully updated')
    
    def test_poem_update_form_invalid(self):
        self.client.force_login(self.test_user)
        form_data = {
            'title': '',
            'translation': ''
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'poetry_translation/poem_update.html')
        self.assertIn('form', response.context)
        self.assertIn('gui_messages', response.context)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Please fill out all the required fields.')


@tag('views', 'views_poetry_poem_delete')
class PoemDeleteViewTestCase(TestCase):
    fixtures = ['test_users.json', 'test_poems.json']
    
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.test_user = cls.User.objects.first()
        cls.test_poem = Poem.objects.first()
        cls.url = reverse('poem_delete', args=[cls.test_poem.pk])
    
    def test_poem_delete_view_as_anonymous_user_POST(self):
        response = self.client.post(self.url, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
    
    def test_poem_delete_view_as_authenticated_user_POST(self):
        self.client.force_login(self.test_user)
        response = self.client.post(self.url, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'poetry_translation/my_library.html')


class AboutViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('about')
        cls.template_name = 'poetry_translation/about.html'
    
    def test_about_view_GET(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)


class SupportUsViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('support_us')
        cls.template_name = 'poetry_translation/support_us.html'
    
    def test_support_us_view_GET(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
    

class PoemLibraryListViewTestCase(TestCase):
    fixtures = ['test_users.json', 'test_poems.json']
    
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('poem_library')
        cls.template_name = 'poetry_translation/poem_library.html'
    
    def test_poem_library_list_view_GET(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context['poems']), 1)
    
    def test_poem_library_list_view_method_not_allowed_POST(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)
        

@tag('views', 'views_poetry_my_library')
class MyLibraryListViewTestCase(TestCase):
    fixtures = ['test_users.json', 'test_poems.json']
    
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.url = reverse('my_library')
        cls.template_name = 'poetry_translation/my_library.html'
        cls.test_user = cls.User.objects.first()
    
    def test_my_library_list_view_GET(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context['poems']), 2)
    
    def test_my_library_list_view_as_anonymous_user_GET(self):
        response = self.client.get(self.url, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('login') + '?next=' + self.url)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertTemplateNotUsed(response, self.template_name)
    
    def test_my_library_list_view_method_not_allowed_POST(self):
        self.client.force_login(self.test_user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)


@tag('views', 'views_poetry_new_features')
class NewFeaturesViewTestCase(TestCase):
    fixtures = ['test_users.json']
    
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.url = reverse('new_features')
        cls.template_name = 'poetry_translation/new_features.html'
        cls.test_user = cls.User.objects.first()
        cls.test_user_staff = cls.User.objects.get(username='test_user_staff')
    
    def test_new_features_view_as_anonymous_user_GET(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('admin:login') + '?next=' + self.url)
        self.assertTemplateNotUsed(response, 'accounts/login.html')
        self.assertTemplateNotUsed(response, self.template_name)
    
    def test_new_features_view_as_unauthorized_user_GET(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('admin:login') + '?next=' + self.url)
        self.assertTemplateNotUsed(response, 'accounts/login.html')
        self.assertTemplateNotUsed(response, self.template_name)
    
    def test_new_features_view_as_staff_user_GET(self):
        self.client.force_login(self.test_user_staff)
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
    

@tag('views', 'views_poetry_test')
class TestViewTestCase(TestCase):
    fixtures = ['test_users.json']
    
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.url = reverse('test')
        cls.template_name = 'poetry_translation/test.html'
        cls.test_user = cls.User.objects.first()
        cls.test_user_staff = cls.User.objects.get(username='test_user_staff')
    
    def test_test_view_as_anonymous_user_GET(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('admin:login') + '?next=' + self.url)
        self.assertTemplateNotUsed(response, 'accounts/login.html')
        self.assertTemplateNotUsed(response, self.template_name)
    
    def test_test_view_as_unauthorized_user_GET(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('admin:login') + '?next=' + self.url)
        self.assertTemplateNotUsed(response, 'accounts/login.html')
        self.assertTemplateNotUsed(response, self.template_name)
    
    def test_test_view_as_staff_user_GET(self):
        self.client.force_login(self.test_user_staff)
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
    
