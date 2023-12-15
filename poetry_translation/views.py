import json

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic import DeleteView, DetailView, ListView, UpdateView, View

from .config import *
from .forms import *
from .models import Poem
from .utils import translate, translate_gpt


class IndexView(View):
    template_name = 'poetry_translation/index.html'
    form_class = ComposePoemForm

    def get(self, request):
        user = request.user
        if user.is_authenticated and user.is_premium:
            character_limit = CHARACTER_LIMIT_PREMIUM
            target_languages = SUPPORTED_LANGUAGES[1:]
        else:
            character_limit = CHARACTER_LIMIT
            target_languages = SUPPORTED_LANGUAGES[1:4]
        
        form_data = {
            'source_languages': SUPPORTED_LANGUAGES,
            'target_languages': target_languages,
            'language_engines': LANGUAGE_ENGINES,
        }
        form = self.form_class(initial=form_data)

        context = {
            'gui_messages': get_gui_messages(['base', 'index']),
            'tooltips': GUI_MESSAGES['tooltips'],
            'language_engines': LANGUAGE_ENGINES,
            'source_languages': SUPPORTED_LANGUAGES,
            'target_languages': target_languages,
            'character_limit': character_limit,
            'form': form
        }
        return render(request, self.template_name, context)


class GetTranslation(View):
    def post(self, request):
        user = request.user
        language_engine = request.POST.get('language_engine')
        source_lang = request.POST.get('source_lang')
        target_lang = request.POST.get('target_lang').lower()
        original_text = request.POST.get('original_text')

        if user.is_authenticated and user.is_premium:
            character_limit = CHARACTER_LIMIT_PREMIUM
        else:
            character_limit = CHARACTER_LIMIT
            
        if language_engine == 'ChatGpt_Poet': # pragma: no cover
            translation = translate_gpt(original_text, target_lang, character_limit)
        
        else:
            translation = translate(
            language_engine,
            source_lang,
            target_lang,
            original_text,
            proxies=None
        )
        return JsonResponse({
            'success': True,
            'translation': translation
        }, safe=False)
    
    
class SaveTranslation(LoginRequiredMixin, View):
    model = Poem
    
    def post(self, request):
        user = request.user
        user_profile = user.profile
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
            saved_by=request.user
        )
        if user_profile.total_poems in (1, 5, 20, 50, 100): # pragma: no cover
            messages.warning(request, GUI_MESSAGES['messages']['badge_earned'])
        
        return HttpResponseRedirect(reverse('poem_update', args=[poem.pk]), {'poem': poem})
    
    
class PoemDetailView(DetailView):
    template_name = 'poetry_translation/poem_detail.html'
    model = Poem
    form_class = PoemDetailForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gui_messages'] = get_gui_messages(['base', 'poem_detail'])
        context['form'] = self.form_class(instance=self.object)
        return context
    
    
class PoemUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'poetry_translation/poem_update.html'
    model = Poem
    form_class = PoemUpdateForm
    success_message = GUI_MESSAGES['messages']['poem_updated']
    error_message = GUI_MESSAGES['error_messages']['poem_update']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gui_messages'] = get_gui_messages(['base', 'poem_detail', 'poem_update'])
        return context
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, self.success_message)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        messages.error(self.request, self.error_message)
        return render(self.request, self.template_name, context)
    
    def get_success_url(self):
        return reverse('poem_detail', args=[self.object.pk])


class PoemDeleteView(SuccessMessageMixin, DeleteView):
    model = Poem
    success_url = reverse_lazy('my_library')
    success_message = GUI_MESSAGES['messages']['poem_deleted']
    
    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class AboutView(View):
    template_name = 'poetry_translation/about.html'

    def get(self, request):
        context = {
            'gui_messages': get_gui_messages(['base', 'about']),
        }
        return render(request, self.template_name, context)


class SupportUsView(View):
    template_name = 'poetry_translation/support_us.html'

    def get(self, request):
        context = {
            'gui_messages': get_gui_messages(['base', 'support_us']),
        }
        return render(request, self.template_name, context)


class PoemLibraryListView(ListView):
    template_name = 'poetry_translation/poem_library.html'
    context_object_name = 'poems'
    model = Poem
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gui_messages'] = get_gui_messages(['base', 'profile', 'table_columns', 'poem_library'])
        return context
    
    def get_queryset(self):
        return self.model.objects.filter(is_hidden=False).order_by('-updated_at')
    
    
class MyLibraryListView(LoginRequiredMixin, ListView):
    template_name = 'poetry_translation/my_library.html'
    context_object_name = 'poems'
    model = Poem
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gui_messages'] = get_gui_messages(['base', 'profile', 'table_columns', 'poem_my_library'])
        return context
    
    def get_queryset(self):
        return self.model.objects.filter(saved_by=self.request.user).order_by('-updated_at')


class NewFeaturesView(View):
    template_name = 'poetry_translation/new_features.html'

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        return render(request, self.template_name, context={'gui_messages': get_gui_messages(['base'])})


class TestView(View):
    template_name = 'poetry_translation/test.html'
    
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        return render(request, self.template_name, context={'gui_messages': get_gui_messages(['base'])})
    