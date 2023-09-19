from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import DeleteView, DetailView, ListView, UpdateView, View

from accounts.models import CustomUser

from .config import *
from .forms import PoemDetailForm, PoemUpdateForm
from .models import Poem
from .utils import translate, translate_gpt


class TranslationFormView(View):
    template_name = 'poetry_translation/index.html'
    language_engine_tooltips = list(LANGUAGE_ENGINE_TOOLTIPS.values())

    def get(self, request):
        context = {
            'target_lang': 'spanish',
            'supported_languages': SUPPORTED_LANGUAGES,
            'language_engines': LANGUAGE_ENGINES,
            'language_engine_tooltips': self.language_engine_tooltips,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        language_engine = request.POST.get('language_engine')
        source_lang = request.POST.get('source_lang')
        target_lang = request.POST.get('target_lang')
        original_text = request.POST.get('original_text')

        if language_engine == 'ChatGpt_Poet':
            translation = translate_gpt(original_text, target_lang)
        
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
            'source_lang': source_lang,
            'target_lang': target_lang,
            'language_engine': language_engine,
            'language_engines': LANGUAGE_ENGINES,
            'language_engine_tooltips': self.language_engine_tooltips,
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
        return self.model.objects.filter(is_hidden=False)
    
    
class MyLibraryView(ListView):
    template_name = 'poetry_translation/my_library.html'
    model = Poem
    
    def get_queryset(self):
        return self.model.objects.filter(saved_by=self.request.user.username)
    

class PoemDetailView(DetailView):
    template_name = 'poetry_translation/poem_detail.html'
    model = Poem
    form_class = PoemDetailForm
    
    def get(self, request, *args, **kwargs):
        poem = self.model.objects.get(pk=kwargs.get('pk'))
        form = self.form_class(instance=poem)
        context = {
            'poem': poem,
            'form': form,
        }
        return render(request, self.template_name, context)


class PoemUpdateView(UpdateView):
    template_name = 'poetry_translation/poem_update.html'
    form_class = PoemUpdateForm
    model = Poem
    
    def get(self, request, *args, **kwargs):
        poem = self.model.objects.get(pk=kwargs.get('pk'))
        form = self.form_class(instance=poem)
        context = {
            'poem': poem,
            'form': form,
        }
        return render(request, self.template_name, context)
    
    def form_valid(self, form):
        if 'edit' in self.request.POST:
            return HttpResponseRedirect(reverse('poem_update', args=[self.object.pk]))
        form.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        messages.success(self.request, _('The poem has been successfully updated.'))
        return reverse('poem_detail', args=[self.object.pk])


class PoemDeleteView(SuccessMessageMixin, DeleteView):
    model = Poem
    success_url = reverse_lazy('my_library')
    success_message = _('The poem has been successfully deleted.')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class SaveTranslation(DetailView):
    model = Poem

    def post(self, request):
        original_text = request.POST.get('original_text')
        translation = request.POST.get('translation')
        source_lang = request.POST.get('source_lang')
        target_lang = request.POST.get('target_lang')
        language_engine = request.POST.get('language_engine')

        poem = Poem.objects.create(
            original_text=original_text,
            translation=translation,
            source_lang=source_lang,
            target_lang=target_lang,
            language_engine=language_engine,
            saved_by=request.user.username
        )
        
        total_poems = Poem.objects.filter(saved_by=request.user.username).count()
        if total_poems in (1, 5, 20, 50, 100):
            messages.warning(request, _('You have earned a badge! Check out your profile!'))
        
        return HttpResponseRedirect(reverse('poem_detail', args=[poem.pk]), {'poem': poem})


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


class TestView(View):
    template_name = 'poetry_translation/test.html'
    
    def get(self, request):
        return render(request, self.template_name)
