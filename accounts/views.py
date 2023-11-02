from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext as _
from django.views.generic import DeleteView, View

from accounts.models import MyProfile
from poetry_translation.config import GUI_MESSAGES
from poetry_translation.models import Poem

from .forms import CustomUserCreationForm, CustomUserLoginForm
from .models import CustomUser
from .tokens import account_activation_token


class SignUpView(View):
    template_name = 'registration/signup.html'
    
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            activate_email(request, user, form.cleaned_data.get('email'))
            return HttpResponseRedirect(reverse('translation'))
     
        return render(request, self.template_name, {'form': form})
    

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


class LoginView(View):
    template_name = 'registration/login.html'
    
    def get(self, request):
        form = CustomUserLoginForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('translation'))
            
        return render(request, self.template_name, {'form': form})


class MyProfileView(View):
    template_name = 'poetry_translation/my_profile.html'
    model = MyProfile
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        total_poems = Poem.objects.filter(saved_by=request.user).count()
        context = {
            'model': self.model,
            'total_poems': total_poems,
            'confirm_account_delete': GUI_MESSAGES['confirm_account_delete'],
        }
        return render(request, self.template_name, context=context)


class DeleteUserView(SuccessMessageMixin, DeleteView):
    model = CustomUser
    success_url = reverse_lazy('translation')    
    success_message = GUI_MESSAGES['messages']['user_deleted']

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
    