from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as authlogin
from django.contrib import messages
from . import forms
# Create your views here
def home(request):
    return render(request, 'base.html')

def professorDashboard(request):
    add_org_form = forms.AddOrganizationToProfessor
    
    context = {
        'add_org_form': add_org_form
    }
    return render(request, 'professor/home.html', context)

def studentDasboard(request):
    
    return render(request, 'student/home.html')

def login(request):
    print('hello', request.method)
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        print(f'user {user}')
        if user and user.is_active:
            authlogin(request,user)

            return redirect(reverse('hrma:professorDashboard')) 
        else:
            messages.error(request,'username or password not correct')
            return redirect(reverse('hrma:login'))
    else:
        form = AuthenticationForm()
    return render(request,'login.html',{'form':form})

class SignUpView(generic.CreateView):
    form_class = forms.SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'