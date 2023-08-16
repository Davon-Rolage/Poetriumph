from django.http import HttpResponseRedirect
from .forms import CustomUserCreationForm
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.contrib.auth import login

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
        