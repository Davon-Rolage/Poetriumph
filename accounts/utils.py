from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core import signing
from django.http import (HttpResponse, HttpResponseNotAllowed,
                         HttpResponseRedirect, JsonResponse)
from django.urls import reverse
from django.utils.timezone import timedelta
from django.views.generic import View

from poetry_translation.config import GUI_MESSAGES

from .models import CustomUserToken, Profile
from .tokens import verify_user_token


def check_username_exists(request):
    if request.method == 'GET':
        username = request.GET.get('username').strip()
        if username:
            exists = get_user_model().objects.filter(username=username).exists()
            return JsonResponse({'exists': exists})
        else:
            return HttpResponse(status=204)

    return HttpResponseNotAllowed(['GET'])
    

class ActivateUserView(View):
    
    def get(self, request, *args, **kwargs):
        token = kwargs.get('token')
        try:
            user_token_instance = CustomUserToken.objects.get(token=token)
            payload = verify_user_token(user_token_instance.user.id, token, max_age=timedelta(days=3))
            
            user_id = payload.get('user_id')
            user = get_user_model().objects.get(id=user_id)
            user.is_active = True
            user.save()
            Profile.objects.create(user=user)
            user_token_instance.delete()
            messages.success(request, GUI_MESSAGES['messages']['activation_successful'])
            return HttpResponseRedirect(reverse('login'))
        
        except CustomUserToken.DoesNotExist:
            messages.error(request, GUI_MESSAGES['error_messages']['activation_failed'])
            return HttpResponseRedirect(reverse('signup'))

        except signing.BadSignature: # pragma: no cover
            messages.error(request, GUI_MESSAGES['error_messages']['activation_failed'])
            user_token_instance.user.delete()
            return HttpResponseRedirect(reverse('signup'))
