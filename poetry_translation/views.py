from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView, ListView, View

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
        user_prompt = request.POST.get('user_prompt')

        if language_engine == 'ChatGpt_Bot':
            translation = translate_gpt(
                source_lang,
                target_lang,
                user_prompt
            )
        else:
            translation = translate(
            language_engine,
            source_lang,
            target_lang,
            user_prompt,
            proxies=None
        )            
        context = {
            'user_prompt': user_prompt,
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
        context = {
            'poetry_translation/premium_features': PREMIUM_FEATURES
        }
        return render(request, self.template_name, context)

class PoemListView(ListView):
    template_name = 'poetry_translation/poem_list.html'
    model = Poem
    paginate_by = 100
    
    def get_queryset(self):
        return self.model.objects.all()
    

class PoemDetailView(DetailView):
    template_name = 'poetry_translation/poem_detail.html'
    model = Poem


class SaveTranslation(DetailView):
    model = Poem

    def post(self, request):
        translation_text = request.POST.get('translation_text')
        language_engine = request.POST.get('language_engine')
        source_lang = request.POST.get('source_lang')
        target_lang = request.POST.get('target_lang')
        user_prompt = request.POST.get('user_prompt')
        title = ' '.join(user_prompt.split(' ', 5)[:5])
        if title.strip() == '':
            title = ' '.join(translation_text.split(' ', 5)[:5])

        poem = Poem.objects.create(
            title=title,
            user_text=user_prompt,
            text=translation_text,
            source_lang=source_lang,
            target_lang=target_lang,
            language_engine=language_engine
        )
        context = {
            'poem': poem
        }
        return HttpResponseRedirect(reverse('poem_detail', args=[poem.pk]), context)

class UpdateTranslation(DetailView):
    model = Poem
    
    def post(self, request, poem_id):
        Poem.objects.filter(pk=poem_id).update(
            user_text=request.POST.get('user_prompt'),
            text=request.POST.get('translation_text'),
            title=request.POST.get('title'),
        )
        return HttpResponseRedirect(reverse('poem_detail', args=(poem_id,)) + '?status_success=true')
