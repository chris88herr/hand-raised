from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as authlogin
from django.contrib import messages
from django.views import View
from hrma.utlis.requestHelper import processProfessorPOSTRequests,processStudentPOSTRequest
from hrma.models import Question, Professor,Organization, Subject, Course, Student
from . import forms
# Create your views here
def home(request):
    return render(request, 'base.html')

class ProfessorDashboard(View):
    template_name = 'professor/home.html'
    context = {}

    def get(self, request, *args, **kwargs):
        self._build_fields(request)
        return render(request, self.template_name , self.context)
    
    def post(self, request, *args, **kwargs):
        self._processPOSTRequest(request)
        self._build_fields(request)
        return render(request, self.template_name, self.context)

    def _processPOSTRequest(self, request):
        processProfessorPOSTRequests(request)

    def _build_fields(self, request):
        print(request)
        add_org_form = forms.AddOrganizationToProfessor
        add_subject_form = forms.AddSubjectToProfessor(user=request.user)
        add_course_form = forms.AddCourseToProfessor(user=request.user)
        professor = Professor.objects.filter(pk=request.user).first()
        professor_orgs = professor.organizations.all()
        professor_subjects = professor.subjects.all()
        professor_courses = Course.objects.prefetch_related('professor__organizations').filter(professor=professor)
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
        
class StudentDasboard(View):
    template_name = 'student/home.html'
    context = {}
    def get(self, request, *args, **kwargs):
        print(f'STUDENT GET REQUEST')
        self._build_fields(request)
        return render(request, self.template_name, self.context)
    
    def post(self, request, *args, **kwargs):
        print(f'REQUEST OBJ --> {request.POST}')
        processStudentPOSTRequest(request)
        self._build_fields(request)
        return render(request, self.template_name, self.context)
        
    def _build_fields(self, request):
        student = Student.objects.filter(pk=request.user).first()
        print(f'collecting forms..')
        add_org_form = forms.AddOrgToStudentForm()
        add_course_form = forms.AddCourseToStudentForm(user = request.user)
        student_orgs = []
        student_professors = []
        student_questions = student.question_set
        student_question_comments = student.questioncomment_set
        student_answers = student.answer_set
        student_answer_comments =student.answercomment_set
        student_courses = student.courses.all()
        for course in student_courses:
            if course.organization not in student_orgs:
                student_orgs.append(course.organization)
            if course.professor not in student_professors:
                student_professors.append(course.professor)
        
        self.context = {
            'add_course_form':add_course_form,
            'add_org_form':add_org_form,
            'student_orgs':student_orgs,
            'student_courses':student_courses,
            'student_professors':student_professors,
            'student_questions' : student_questions,
            'student_question_comments' : student_question_comments,
            'student_answers' : student_answers,
            'student_answer_comments' : student_answer_comments
        }

class CoursesView(View):
    template_name = 'student/student_course.html'
    context = {}
    def get(self, request, *args, **kwargs):
        self._build_fields(request, kwargs)
        return render(request, self.template_name , self.context)

    def _build_fields(self, request, kwargs):
        course_id = kwargs.pop('course_id')
        self.context = {
            'course_id':course_id
        }     
    
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        print(f'user {user}')
        if user and user.is_active:
            authlogin(request,user)
            if user.is_professor:
                return redirect(reverse('hrma:professorDashboard')) 
            else:
                return redirect(reverse('hrma:studentDashboard')) 

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