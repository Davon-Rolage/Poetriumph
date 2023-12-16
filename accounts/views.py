from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import DeleteView, FormView, View

from accounts.models import CustomUserToken, Profile
from poetry_translation.config import get_gui_messages

from .forms import CustomUserCreationForm, CustomUserLoginForm
from .models import CustomUser
from .tokens import account_activation_token
from .utils import *


class SignUpView(FormView):
    template_name = 'accounts/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('translation')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gui_messages'] = get_gui_messages(['base', 'accounts'])
        return context
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        user_token = CustomUserToken.objects.create(
            user=user,
            token=account_activation_token.make_token(user),
        )
        form.send_activation_email(self.request, user, user_token.token)
        success_message = GUI_MESSAGES['messages']['email_sent'].format(
            user=user, to_email=form.cleaned_data.get('email')
        )
        messages.success(self.request, success_message)
        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = CustomUserLoginForm
    success_url = reverse_lazy('translation')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gui_messages'] = get_gui_messages(['base', 'accounts'])
        return context
    
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        login(self.request, authenticate(username=username, password=password))
        return super().form_valid(form)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('translation'))


class ProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'
    model = Profile
    
    def get(self, request):
        badge_count = [1, 5, 20, 50, 100]
        user_profile = request.user.profile
        context = {
            'gui_messages': get_gui_messages(['base', 'profile', 'total_poems']),
            'badge_count': badge_count,
            'user_profile': user_profile,
        }
        return render(request, self.template_name, context=context)


class DeleteUserView(SuccessMessageMixin, DeleteView):
    model = CustomUser
    success_url = reverse_lazy('translation')    
    success_message = GUI_MESSAGES['messages']['user_deleted']
    
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
        CustomUser.objects.filter(username=user.username).update(is_premium=True)
        return HttpResponseRedirect(reverse('premium'))


class CancelPremiumView(View):
    model = CustomUser
    
    def post(self, request):
        user = request.user
        CustomUser.objects.filter(username=user.username).update(is_premium=False)
        return HttpResponseRedirect(reverse('premium'))
