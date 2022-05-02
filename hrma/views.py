from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as authlogin
from django.contrib import messages
from django.views import View
from hrma.utlis.views import processProfessorPOSTRequests
from hrma.models import Professor,Organization, Subject, Course
from . import forms
# Create your views here
def home(request):
    return render(request, 'base.html')

class ProfessorDashboard(View):
    template_name = 'professor/home.html'
    
    def get(self, request, *args, **kwargs):
        print(f'template name {self.template_name}')
        self._build_fields(request)
        return render(request, self.template_name , self.context)
    
    def post(self, request, *args, **kwargs):
        self._processPOSTRequest(request)
        self._build_fields(request)
        return render(request, self.template_name, self.context)

    def _processPOSTRequest(self, request):
        print(f'{request}:{request.POST}')
        processProfessorPOSTRequests(request)

    def _build_fields(self, request):
        add_org_form = forms.AddOrganizationToProfessor
        add_subject_form = forms.AddSubjectToProfessor(user=request.user)
        add_course_form = forms.AddCourseToProfessor(user=request.user)
        professor = Professor.objects.filter(pk=request.user).first()
        professor_orgs = professor.organizations.all()
        professor_subjects = professor.subjects.all()
        professor_courses = Course.objects.select_related().filter(professor=professor)
        print(f'professor\'s courses {professor_courses}')
        print(f'professor\'s orgs passed to template: {professor_orgs}')
        self.context = {
            'professor_courses':professor_courses,
            'professor_orgs':professor_orgs,
            'professor_subjects':professor_subjects,
            'add_course_form':add_course_form,
            'add_org_form': add_org_form,
            'add_subject_form':add_subject_form
        }
        
def studentDasboard(request):
    return render(request, 'student/home.html')

def login(request):
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