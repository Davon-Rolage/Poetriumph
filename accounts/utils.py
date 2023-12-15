from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import (HttpResponse, HttpResponseNotAllowed,
                         HttpResponseRedirect, JsonResponse)
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from poetry_translation.config import GUI_MESSAGES

from .models import CustomUser, CustomUserToken, Profile
from django.views.generic import View
from .tokens import account_activation_token


def check_username_exists(request):
    if request.method == 'GET':
        username = request.GET.get('username').strip()
        if username:
            exists = CustomUser.objects.filter(username=username).exists()
            return JsonResponse({'exists': exists})
        else:
            return HttpResponse(status=204)
    return HttpResponseNotAllowed(['GET'])
    
    
class ActivateUserView(View):
    
    def get(self, request, *args, **kwargs):
        token = kwargs.get('token')
        try:
            user_token_instance = CustomUserToken.objects.get(token=token)
            user = user_token_instance.user
            if not user_token_instance.is_expired:
                user.is_active = True
                user.save()
                Profile.objects.create(user=user)
                user_token_instance.delete()
                messages.success(request, GUI_MESSAGES['messages']['activation_successful'])
                return HttpResponseRedirect(reverse('login'))
            else:
                user_token_instance.delete()
        
        except CustomUserToken.DoesNotExist:
            pass
            
        messages.error(request, GUI_MESSAGES['error_messages']['activation_failed'])
        return HttpResponseRedirect(reverse('signup'))
