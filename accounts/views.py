from django.http import HttpResponseRedirect
from .forms import CustomUserCreationForm, CustomUserLoginForm
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.contrib.auth import login, authenticate


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
