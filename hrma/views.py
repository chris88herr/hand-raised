from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from . import forms
# Create your views here.
def home(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')

class SignUpView(generic.CreateView):
    form_class = forms.SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'