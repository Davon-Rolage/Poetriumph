from django.test import SimpleTestCase, tag
from django.urls import resolve, reverse

from poetry_translation.views import *


@tag('urls', 'urls_poetry')
class PoetryUrlTestCase(SimpleTestCase):
    
    def test_translation_url_resolves(self):
        url = reverse('translation')
        self.assertEqual(resolve(url).func.view_class, IndexView)
    
    def test_about_url_resolves(self):
        url = reverse('about')
        self.assertEqual(resolve(url).func.view_class, AboutView)
    
    def test_support_us_url_resolves(self):
        url = reverse('support_us')
        self.assertEqual(resolve(url).func.view_class, SupportUsView)
    
    def test_get_translation_url_resolves(self):
        url = reverse('get_translation')
        self.assertEqual(resolve(url).func.view_class, GetTranslation)
    
    def test_save_translation_url_resolves(self):
        url = reverse('save_translation')
        self.assertEqual(resolve(url).func.view_class, SaveTranslation)
    
    def test_poem_library_url_resolves(self):
        url = reverse('poem_library')
        self.assertEqual(resolve(url).func.view_class, PoemLibraryListView)
    
    def test_poem_detail_url_resolves(self):
        url = reverse('poem_detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, PoemDetailView)
    
    def test_poem_update_url_resolves(self):
        url = reverse('poem_update', args=[1])
        self.assertEqual(resolve(url).func.view_class, PoemUpdateView)
    
    def test_poem_delete_url_resolves(self):
        url = reverse('poem_delete', args=[1])
        self.assertEqual(resolve(url).func.view_class, PoemDeleteView)
    
    def test_my_library_url_resolves(self):
        url = reverse('my_library')
        self.assertEqual(resolve(url).func.view_class, MyLibraryListView)
    
    def test_new_features_url_resolves(self):
        url = reverse('new_features')
        self.assertEqual(resolve(url).func.view_class, NewFeaturesView)
    
    def test_test_url_resolves(self):
        url = reverse('test')
        self.assertEqual(resolve(url).func.view_class, TestView)
