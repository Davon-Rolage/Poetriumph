from django.test import TestCase, tag
from poetry_translation.models import Poem
from django.contrib.auth import get_user_model


@tag('model', 'model_poetry')
class PoemTestCase(TestCase):
    fixtures = ['test_poems.json', 'test_users.json']

    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.test_poem = Poem.objects.get(pk=1)
        cls.user = cls.User.objects.first()
        
        cls.default_poem = Poem.objects.create(
            author='default_author',
            saved_by=cls.user
        )
    
    def test_poem_model_str(self):
        self.assertEqual(str(self.test_poem), 'test_title')
    
    def test_poem_model_default_str(self):
        self.assertEqual(self.default_poem.title, 'Untitled')
        self.assertEqual(str(self.default_poem), '3 - test_user')
        self.assertTrue(self.default_poem.is_hidden)
        self.assertFalse(self.default_poem.original_text)
        self.assertFalse(self.default_poem.translation)
    