from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
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
        user = request.user
        if user.is_authenticated and user.is_premium:
            character_limit = CHARACTER_LIMIT_PREMIUM
        else:
            character_limit = CHARACTER_LIMIT
            
        context = {
            'target_lang': 'spanish',
            'supported_languages': SUPPORTED_LANGUAGES,
            'language_engines': LANGUAGE_ENGINES,
            'language_engine_tooltips': self.language_engine_tooltips,
            'character_limit': character_limit,
            'loading_button_text': GUI_MESSAGES['loading_button_text'],
            'loading_tooltip_text': GUI_MESSAGES['loading_tooltip_text'],
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user
        language_engine = request.POST.get('language_engine')
        source_lang = request.POST.get('source_lang')
        target_lang = request.POST.get('target_lang')
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
         
        context = {
            'original_text': original_text,
            'translation': translation,
            'supported_languages': SUPPORTED_LANGUAGES,
            'source_lang': source_lang,
            'target_lang': target_lang,
            'language_engine': language_engine,
            'language_engines': LANGUAGE_ENGINES,
            'language_engine_tooltips': self.language_engine_tooltips,
            'character_limit': character_limit,
            'loading_button_text': GUI_MESSAGES['loading_button_text'],
            'loading_tooltip_text': GUI_MESSAGES['loading_tooltip_text'],
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
        return self.model.objects.filter(is_hidden=False).order_by('-updated_at')
    
    
class MyLibraryView(ListView):
    template_name = 'poetry_translation/my_library.html'
    model = Poem
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return self.model.objects.filter(saved_by=self.request.user.username).order_by('-updated_at')
    

class PoemDetailView(DetailView):
    template_name = 'poetry_translation/poem_detail.html'
    model = Poem
    form_class = PoemDetailForm
    
    def get(self, request, *args, **kwargs):
        poem = get_object_or_404(self.model, pk=kwargs.get('pk'))
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
    success_message = GUI_MESSAGES['messages']['poem_updated']
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        poem = get_object_or_404(self.model, pk=kwargs.get('pk'))
        form = self.form_class(instance=poem)
        context = {
            'poem': poem,
            'form': form,
            'confirm_poem_delete': GUI_MESSAGES['confirm_poem_delete'],
        }
        return render(request, self.template_name, context)
    
    def form_valid(self, form):
        if 'edit' in self.request.POST:
            return HttpResponseRedirect(reverse('poem_update', args=[self.object.pk]))
        form.save()
        messages.success(self.request, self.success_message)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('poem_detail', args=[self.object.pk])


class PoemDeleteView(SuccessMessageMixin, DeleteView):
    model = Poem
    success_url = reverse_lazy('my_library')
    success_message = GUI_MESSAGES['messages']['poem_deleted']
    
    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class SaveTranslation(DetailView):
    model = Poem

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
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

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        return render(request, self.template_name)


class TestView(View):
    template_name = 'poetry_translation/test.html'
    
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        return render(request, self.template_name)
