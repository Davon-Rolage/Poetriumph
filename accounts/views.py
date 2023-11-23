from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import DeleteView, View

from accounts.models import MyProfile
from poetry_translation.config import GUI_MESSAGES
from poetry_translation.models import Poem

from .forms import CustomUserCreationForm, CustomUserLoginForm
from .models import CustomUser
from .utils import *


class SignUpView(View):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm
        
    def get(self, request):
        form = self.form_class()
        context = {
            'gui_messages': GUI_MESSAGES['base'] | GUI_MESSAGES['accounts'],
            'form': form
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            activate_email(request, user, form.cleaned_data.get('email'))
            return HttpResponseRedirect(reverse('translation'))

        context = {
            'gui_messages': GUI_MESSAGES['base'] | GUI_MESSAGES['accounts'],
            'form': form
        }
        return render(request, self.template_name, context)


class LoginView(View):
    template_name = 'registration/login.html'
    
    def get(self, request):
        form = CustomUserLoginForm()
        context = {
            'gui_messages': GUI_MESSAGES['base'] | GUI_MESSAGES['accounts'],
            'form': form
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('translation'))
            
        context = {
            'gui_messages': GUI_MESSAGES['base'] | GUI_MESSAGES['accounts'],
            'form': form
        }
        return render(request, self.template_name, context)


class MyProfileView(View):
    template_name = 'poetry_translation/my_profile.html'
    model = MyProfile
    
    def get(self, request):
        total_poems = Poem.objects.filter(saved_by=request.user).count()
        badge_count = [1, 5, 20, 50, 100]
        context = {
            'total_poems': total_poems,
            'badge_count': badge_count,
            'gui_messages': GUI_MESSAGES['base']
                          | GUI_MESSAGES['my_profile']
                          | { 'total_poems': GUI_MESSAGES['total_poems'] },
        }
        return render(request, self.template_name, context=context)


class DeleteUserView(SuccessMessageMixin, DeleteView):
    model = CustomUser
    success_url = reverse_lazy('translation')    
    success_message = GUI_MESSAGES['messages']['user_deleted']

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
    