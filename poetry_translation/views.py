import os
from django.http import HttpResponseRedirect

from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View, ListView, DetailView
from .models import Poem

from .config import *
from .utils import translate, translate_gpt


class TranslationFormView(View):
    template_name = 'index.html'

    def get(self, request):
        context = {
            'source_lang': 'auto',
            'target_lang': 'english',
            'language_engine': SUPPORTED_LANGUAGES[0],
            'supported_languages': SUPPORTED_LANGUAGES,
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
    template_name = 'about.html'

    def get(self, request):
        return render(request, self.template_name)


class SupportUsView(View):
    template_name = 'support_us.html'

    def get(self, request):
        return render(request, self.template_name)


class PremiumView(View):
    template_name = 'premium.html'

    def get(self, request):
        return render(request, self.template_name)

class PoemListView(ListView):
    template_name = 'poem_list.html'
    model = Poem
    paginate_by = 10
    
    def get_queryset(self):
        return self.model.objects.all()
    

class PoemDetailView(DetailView):
    template_name = 'poem_detail.html'
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

        # Create a new Poem object and save it to the database
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
    
    def post(self, request):
        print(f'''POEM OK''')
        # poem = self.model.objects.filter(pk=self.kwargs['pk'])
        poem = self.model.objects.get(pk=self.kwargs['pk'])
        
        poem.title = request.POST.get('title')
        poem.user_prompt = request.POST.get('user_prompt')
        poem.translation_text = request.POST.get('translation_text')
        poem.language_engine = request.POST.get('language_engine')
        poem.source_lang = request.POST.get('source_lang')
        poem.target_lang = request.POST.get('target_lang')
        poem.save()

        # poem = Poem.objects.update(
        #     title=title,
        #     user_text=user_prompt,
        #     text=translation_text,
        #     source_lang=source_lang,
        #     target_lang=target_lang,
        #     language_engine=language_engine
        # )

        return HttpResponseRedirect(reverse('poem_detail', args=[poem.pk]))