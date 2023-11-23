import json

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic import DeleteView, DetailView, ListView, UpdateView, View

from accounts.models import CustomUser

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
            'gui_messages': GUI_MESSAGES['base'] | GUI_MESSAGES['index'],
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
            
        if language_engine == 'ChatGpt_Poet':
            translation = translate_gpt(original_text, target_lang, character_limit)
        
        else:
            translation = translate(
            language_engine,
            source_lang,
            target_lang,
            original_text,
            proxies=None
        )
        json_data = json.dumps([
            {
                'success': 'true',
                'translation': translation
            }
        ])
        return HttpResponse(json_data)
    
    
class SaveTranslation(LoginRequiredMixin, DetailView):
    model = Poem
    
    def post(self, request):
        user = request.user
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
        
        total_poems = Poem.objects.filter(saved_by=user.username).count()
        if total_poems in (1, 5, 20, 50, 100):
            messages.warning(request, GUI_MESSAGES['messages']['badge_earned'])
        
        return HttpResponseRedirect(reverse('poem_update', args=[poem.pk]), {'poem': poem})
    
    
class PoemDetailView(DetailView):
    template_name = 'poetry_translation/poem_detail.html'
    model = Poem
    form_class = PoemDetailForm
    
    def get(self, request, *args, **kwargs):
        poem = get_object_or_404(self.model, pk=kwargs.get('pk'))
        form = self.form_class(instance=poem)
        context = {
            'gui_messages': GUI_MESSAGES['base'] | GUI_MESSAGES['poem_detail'],
            'poem': poem,
            'form': form,
        }
        return render(request, self.template_name, context)


class PoemUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'poetry_translation/poem_update.html'
    form_class = PoemUpdateForm
    model = Poem
    success_message = GUI_MESSAGES['messages']['poem_updated']
    
    def get(self, request, *args, **kwargs):
        poem = get_object_or_404(self.model, pk=kwargs.get('pk'))
        form = self.form_class(instance=poem)
        context = {
            'gui_messages': GUI_MESSAGES['base'] | GUI_MESSAGES['poem_detail'] | GUI_MESSAGES['poem_update'],
            'poem': poem,
            'form': form,
        }
        return render(request, self.template_name, context)
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, self.success_message)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        context = {
            'gui_messages': GUI_MESSAGES['base'] | GUI_MESSAGES['poem_detail'] | GUI_MESSAGES['poem_update'],
            'poem': self.object,
            'form': form
        }
        messages.error(self.request, GUI_MESSAGES['error_messages']['poem_update'])
        return render(self.request, self.template_name, context)
    
    def get_success_url(self):
        return reverse('poem_detail', args=[self.object.pk])


class AboutView(View):
    template_name = 'poetry_translation/about.html'

    def get(self, request):
        context = {
            'gui_messages': GUI_MESSAGES['base'] | GUI_MESSAGES['about'],
        }
        return render(request, self.template_name, context)


class SupportUsView(View):
    template_name = 'poetry_translation/support_us.html'

    def get(self, request):
        context = {
            'gui_messages': GUI_MESSAGES['base'] | GUI_MESSAGES['support_us'],
        }
        return render(request, self.template_name, context)


class PoemLibraryListView(ListView):
    template_name = 'poetry_translation/poem_library.html'
    model = Poem
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {'poems': self.get_queryset(),
            'gui_messages': GUI_MESSAGES['base'] 
                          | GUI_MESSAGES['table_columns'] 
                          | { 'total_poems': GUI_MESSAGES['total_poems'] }
                          | { 'poem_library_title': GUI_MESSAGES['poem_library_title'] }
        }
        return context
    
    def get_queryset(self):
        return self.model.objects.filter(is_hidden=False).order_by('-updated_at')
    
    
class MyLibraryView(LoginRequiredMixin, ListView):
    template_name = 'poetry_translation/my_library.html'
    model = Poem
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {'poems': self.get_queryset(),
            'gui_messages': GUI_MESSAGES['base'] 
                          | GUI_MESSAGES['table_columns'] 
                          | { 'my_library_title': GUI_MESSAGES['my_library_title'] }
                          | { 'total_poems': GUI_MESSAGES['total_poems'] }
        }
        return context
    
    def get_queryset(self):
        return self.model.objects.filter(saved_by=self.request.user.username).order_by('-updated_at')


class PoemDeleteView(SuccessMessageMixin, DeleteView):
    model = Poem
    success_url = reverse_lazy('my_library')
    success_message = GUI_MESSAGES['messages']['poem_deleted']
    
    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class PremiumView(View):
    template_name = 'poetry_translation/premium.html'

    def get(self, request):
        context = {
            'gui_messages': GUI_MESSAGES['base'] | GUI_MESSAGES['premium'],
        }
        return render(request, self.template_name, context)


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

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        return render(request, self.template_name, context={'gui_messages': GUI_MESSAGES['base']})


class TestView(View):
    template_name = 'poetry_translation/test.html'
    
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        return render(request, self.template_name, context={'gui_messages': GUI_MESSAGES['base']})
    