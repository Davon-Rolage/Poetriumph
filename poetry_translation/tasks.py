from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string

from accounts.models import CustomUserToken
from poetry_translation.config import GUI_MESSAGES


@shared_task()
def send_activation_email_task(user_id=None, domain=None, protocol=None, to_email=None):
    mail_subject = GUI_MESSAGES['messages']['email_subject']
    user = get_user_model().objects.get(id=user_id)
    user_token = CustomUserToken.objects.get(user=user).token
    
    message = render_to_string('accounts/activate_email.html', {
        'username': user.get_username(),
        'domain': domain,
        'token': user_token,
        'protocol': protocol
    })
    send_mail(
        mail_subject, message, html_message=message,
        from_email=None, recipient_list=[to_email]
    )
