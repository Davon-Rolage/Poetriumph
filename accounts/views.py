from django.contrib import messages
from django.contrib.auth import (authenticate, get_user_model, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import FormView, RedirectView, View

from poetry_translation.config import get_gui_messages

from .forms import *
from .models import CustomUserTokenType
from .tokens import generate_user_token
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
        email = form.cleaned_data.get('email')
        token_type = CustomUserTokenType.objects.first()
        CustomUserToken.objects.create(
            user=user,
            token=generate_user_token(user.id),
            token_type=token_type,
        )
        domain = self.request.get_host()
        protocol = self.request.scheme
        language = self.request.LANGUAGE_CODE
        form.send_activation_email(
            user_id=user.id,
            domain=domain,
            protocol=protocol,
            to_email=email,
            language=language
        )
        success_message = GUI_MESSAGES['messages']['activation_email_sent'].format(
            user=user, to_email=email
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
        
        stay_signed_in = form.cleaned_data.get('stay_signed_in')
        if stay_signed_in:
            self.request.session.set_expiry(None) # default 14 days
        else:
            self.request.session.set_expiry(0) # until browser is closed
            # Some browsers, like Chrome, can interfere with session expiration on browser close:
            # https://docs.djangoproject.com/en/4.2/topics/http/sessions/#browser-length-sessions-vs-persistent-sessions
        return super().form_valid(form)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('translation'))


class ProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'
    
    def get(self, request):
        user = request.user
        user_profile = user.profile        
        context = {
            'gui_messages': get_gui_messages(['base', 'profile', 'tooltips']),
            'user_profile': user_profile
        }
        return render(request, self.template_name, context=context)


class DeactivateUserView(SuccessMessageMixin, View):
    def post(self, request):
        user = request.user
        user.is_active = False
        user.email = ''
        user.username += f' - deactivated {user.id}'
        user.save()
        update_session_auth_hash(request, user)
        logout(request)
        messages.success(self.request, GUI_MESSAGES['messages']['user_deactivated'])
        return HttpResponseRedirect(reverse_lazy('translation'))
    

class PasswordResetView(FormView):
    template_name = 'accounts/password_reset.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('translation')
    token_generator = PasswordResetTokenGenerator()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gui_messages'] = get_gui_messages(['base', 'accounts'])
        return context
    
    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        user = get_user_model().objects.get(email=email)
        token_type = CustomUserTokenType.objects.get(name='Password reset')
        CustomUserToken.objects.filter(
            user=user,
            token_type=token_type
        ).delete()
        CustomUserToken.objects.create(
            user=user,
            token=self.token_generator.make_token(user),
            token_type=token_type,
        )
        domain = self.request.get_host()
        protocol = self.request.scheme
        language = self.request.LANGUAGE_CODE
        form.send_password_reset_email(
            user_id=user.id,
            domain=domain,
            protocol=protocol,
            to_email=email,
            language=language
        )
        success_message = GUI_MESSAGES['messages']['password_reset_email_sent'].format(
            to_email=email
        )
        messages.success(self.request, success_message)
        return super().form_valid(form)


class PasswordResetCheckView(RedirectView):
    def get_redirect_url(self, token):
        token_generator = PasswordResetTokenGenerator()
        try:
            user_token = CustomUserToken.objects.get(token=token)
            user = user_token.user

            if token_generator.check_token(user, token):
                return reverse('set_password', args=[token])
            else:
                messages.error(self.request, GUI_MESSAGES['error_messages']['password_reset_failed'])
                user_token.delete()

        except (ValueError, CustomUserToken.DoesNotExist):
            messages.error(self.request, GUI_MESSAGES['error_messages']['password_reset_failed'])

        except signing.BadSignature: # pragma: no cover
            messages.error(self.request, GUI_MESSAGES['error_messages']['password_reset_failed'])
            user_token.delete()

        return reverse('login')


class SetPasswordView(FormView):
    template_name = 'accounts/password_set.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gui_messages'] = get_gui_messages(['base', 'accounts'])
        return context
    
    def form_valid(self, form):
        token = self.kwargs.get('token')
        token_instance = CustomUserToken.objects.get(token=token)
        user = token_instance.user
        
        user.set_password(form.cleaned_data.get('password1'))
        user.save()
        
        messages.success(self.request, GUI_MESSAGES['messages']['password_reset_successful'])
        token_instance.delete()
        return super().form_valid(form)


class PremiumView(View):
    template_name = 'poetry_translation/premium.html'

    def get(self, request):
        context = {
            'gui_messages': get_gui_messages(['base', 'premium']),
        }
        return render(request, self.template_name, context)


class GetPremiumView(LoginRequiredMixin, View):
    model = get_user_model()

    def post(self, request):
        user = request.user
        if not user.is_premium:
            user.is_premium = True
            user.save()
        return JsonResponse({'success': True})


class CancelPremiumView(View):
    model = get_user_model()

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            user.is_premium = False
            user.save()
        return HttpResponseRedirect(reverse('premium'))
