from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import DetailView, ListView, View

from accounts.models import CustomUser

from .config import *
from .models import Poem
from .utils import translate, translate_gpt


class TranslationFormView(View):
    template_name = 'poetry_translation/index.html'

    def get(self, request):
        supported_languages = SUPPORTED_LANGUAGES
        if not (request.user.is_authenticated and request.user.is_premium):
            supported_languages = supported_languages[:4]
            
        context = {
            'source_lang': 'auto',
            'target_lang': 'english',
            'language_engine': SUPPORTED_LANGUAGES[0],
            'supported_languages': supported_languages,
            'language_engines': LANGUAGE_ENGINES,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        language_engine = request.POST.get('language_engine')
        source_lang = request.POST.get('source_lang')
        target_lang = request.POST.get('target_lang')
        original_text = request.POST.get('original_text')

        if language_engine == 'ChatGpt_Poet':
            translation = translate_gpt(
                source_lang,
                target_lang,
                original_text
            )
        else:
            translation = translate(
            language_engine,
            source_lang,
            target_lang,
            original_text,
            proxies=None
        )            
        context = {
            'original_text': original_text,
            'translation': translation,
            'supported_languages': SUPPORTED_LANGUAGES,
            'language_engines': LANGUAGE_ENGINES,
            'source_lang': source_lang,
            'target_lang': target_lang,
            'language_engine': language_engine,
        }
        return render(request, self.template_name, context)


class AboutView(View):
    template_name = 'poetry_translation/about.html'

    def get(self, request):
        return render(request, self.template_name)


class SupportUsView(View):
    template_name = 'poetry_translation/support_us.html'

    def get(self, request):
        return render(request, self.template_name)


class PremiumView(View):
    template_name = 'poetry_translation/premium.html'

    def get(self, request):
        return render(request, self.template_name)


class PoemListView(ListView):
    template_name = 'poetry_translation/poem_library.html'
    model = Poem
    paginate_by = 100
    
    def get_queryset(self):
        return self.model.objects.all()
    
    
class MyLibraryView(ListView):
    template_name = 'poetry_translation/my_library.html'
    model = Poem
    
    def get_queryset(self):
        return self.model.objects.filter(saved_by=self.request.user.username)
    

class PoemDetailView(DetailView):
    template_name = 'poetry_translation/poem_detail.html'
    model = Poem


class SaveTranslation(DetailView):
    model = Poem

    def post(self, request):
        original_text = request.POST.get('original_text')
        translation = request.POST.get('translation')
        source_lang = request.POST.get('source_lang')
        target_lang = request.POST.get('target_lang')
        language_engine = request.POST.get('language_engine')
        title = ' '.join(original_text.split(' ', 5)[:5])
        if title.strip() == '':
            title = ' '.join(translation.split(' ', 5)[:5])

        poem = Poem.objects.create(
            title=title,
            original_text=original_text,
            translation=translation,
            source_lang=source_lang,
            target_lang=target_lang,
            language_engine=language_engine,
            saved_by=request.user.username
        )
        context = {
            'poem': poem
        }
        return HttpResponseRedirect(reverse('poem_detail', args=[poem.pk]), context)


class UpdateTranslation(DetailView):
    model = Poem
    
    def post(self, request, poem_id):
        Poem.objects.filter(pk=poem_id).update(
            original_text=request.POST.get('original_text'),
            translation=request.POST.get('translation_text'),
            title=request.POST.get('title'),
            author=request.POST.get('author'),
            saved_by=request.user.username
        )
        return HttpResponseRedirect(reverse('poem_detail', args=(poem_id,)) + '?status_success=true')
    

class DeleteTranslation(DetailView):
    model = Poem
    
    def post(self, request, poem_id):
        Poem.objects.filter(pk=poem_id).delete()
        return HttpResponseRedirect(reverse('my_library'))


class GetPremiumView(View):
    model = CustomUser
    
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            CustomUser.objects.filter(username=user.username).update(is_premium=True)
        return HttpResponseRedirect(reverse('premium'))


class CancelPremiumView(View):
    model = CustomUser
    
    def post(self, request):
        user = request.user
        CustomUser.objects.filter(username=user.username).update(is_premium=False)
        return HttpResponseRedirect(reverse('premium'))


class NewFeaturesView(View):
    template_name = 'poetry_translation/new_features.html'
    
    def get(self, request):
        return render(request, self.template_name)
