from django.contrib import messages
from django.contrib.auth import authenticate, login
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


class SignUpView(View):
    template_name = 'registration/signup.html'
    
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            login(request, form.instance)
            return HttpResponseRedirect(reverse('translation'))
     
        return render(request, self.template_name, {'form': form})


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
    