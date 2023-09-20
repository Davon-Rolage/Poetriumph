from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import DeleteView, View

from accounts.models import MyProfile
from poetry_translation.models import Poem

from .forms import CustomUserCreationForm, CustomUserLoginForm
from .models import CustomUser
from .tokens import account_activation_token

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage


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
        
        messages.success(request, _('Thank you for your email confirmation. Now you can login your account.'))
        return HttpResponseRedirect(reverse('login'))
    else:
        messages.error(request, _('Activation link is invalid!'))
    
    return HttpResponseRedirect(reverse('translation'))
    

def activate_email(request, user, to_email):
    mail_subject = _('Activate your account')
    message = render_to_string('registration/activate_email.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, _(f'<b>{user}</b>, please check your email <b>{to_email}</b> to activate your account.'))
    else:
        messages.error(request, _(f'Problem sending email to <b>{to_email}</b>, please try again.'))


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
    
    def get(self, request):
        total_poems = Poem.objects.filter(saved_by=request.user).count()
        context = {
            'model': self.model,
            'total_poems': total_poems,
        }
        return render(request, self.template_name, context=context)


class DeleteUserView(SuccessMessageMixin, DeleteView):
    model = CustomUser
    success_url = reverse_lazy('translation')    
    success_message = _('The user has been successfully deleted.')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
    