from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from poetry_translation.config import GUI_MESSAGES

from .models import CustomUser
from .tokens import account_activation_token


def check_username_exists(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        if CustomUser.objects.filter(username=username).exists():
            return HttpResponse('true')
        else:
            return HttpResponse('false')
    
    
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        
        messages.success(request, GUI_MESSAGES['messages']['activation_successful'])
        return HttpResponseRedirect(reverse('login'))
    else:
        messages.error(request, GUI_MESSAGES['error_messages']['activation_failed'])
    
    return HttpResponseRedirect(reverse('translation'))
    

def activate_email(request, user, to_email):
    mail_subject = GUI_MESSAGES['messages']['email_subject']
    message = render_to_string('registration/activate_email.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        success_message = GUI_MESSAGES['messages']['email_sent'].format(user=user, to_email=to_email)
        messages.success(request, success_message)
    else:
        messages.error(request, GUI_MESSAGES['error_messages']['email_sent'].format(to_email=to_email))
        