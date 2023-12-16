from django.contrib import messages
from django.http import (HttpResponse, HttpResponseNotAllowed,
                         HttpResponseRedirect, JsonResponse)
from django.urls import reverse
from django.views.generic import View

from poetry_translation.config import GUI_MESSAGES

from .models import CustomUser, CustomUserToken, Profile


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
            user.is_active = True
            user.save()
            Profile.objects.create(user=user)
            user_token_instance.delete()
            messages.success(request, GUI_MESSAGES['messages']['activation_successful'])
            return HttpResponseRedirect(reverse('login'))
        
        except CustomUserToken.DoesNotExist:
            messages.error(request, GUI_MESSAGES['error_messages']['activation_failed'])
            return HttpResponseRedirect(reverse('signup'))
