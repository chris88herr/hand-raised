from ctypes import windll
from lib2to3.pgen2.token import LBRACE
from turtle import textinput
from django.contrib.auth.forms import UserCreationForm
from pkg_resources import require
from hrma.models import Subject
from hrma.models import User
from django import forms
from hrma.models import Student, Professor, Organization
from django.db.models.query import QuerySet
from itertools import chain
STUDENT = 1
PROFESSOR = 2
USER_TYPES = (
    (STUDENT, 'Student'),
    (PROFESSOR, 'Professor')
)
class SignUpForm(UserCreationForm):
    userType = forms.CharField(label='You are a: ', widget=forms.Select(choices=USER_TYPES))
    email = forms.CharField(label='Email', widget=forms.TextInput())
    password1 = forms.CharField(label='Enter password', 
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', 
                                widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1','password2', 'userType')
        help_texts = {
            'username': None,
        }

    def save(self, commit=True):
        user = super().save()
        userType = user.userType
                
        if int(userType) == STUDENT:
            user.is_student = True
            print(f'creating student {user}')
            Student.objects.create(user=user)
        else:
            user.is_professor = True
            print(f'creating professor {user}')
            Professor.objects.create(user=user)

        if commit:
            user.save()
        return user

class AddOrganizationToProfessor(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super(AddOrganizationToProfessor, self).__init__(*args, **kwargs)
        self._build_fields()

    def _build_fields(self):
        orgs = Organization.objects.all()
        print(f'Add Org Form orgs {orgs}')
        self.fields['organizations'] = forms.ModelChoiceField(
            queryset=orgs
        )
        # self.fields['professor'].initial = Professor.objects.filter(pk=self.user).first()
        # self.fields['professor'].widget = forms.HiddenInput()

class AddSubjectToProfessor(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(AddSubjectToProfessor, self).__init__(*args, **kwargs)
        self._build_fields()

    def _build_fields(self):
        professor = Professor.objects.filter(pk=self.user).first()
        print(f'professor {professor}')
        if professor.organizations:
            orgs = professor.organizations.all()
            print(f'professor\'s orgs {orgs}')
            self.fields['organizations'] = forms.ModelChoiceField(queryset=orgs)
            subjectsList = []
            for org in orgs:
                subjectsList.append(Subject.objects.filter(organization=org))
            if len(subjectsList)>0:
                subjects = QuerySet.union(*subjectsList)
                self.fields['subjects'] = forms.ModelChoiceField(queryset=subjects)
            else:
                self.fields['subjects'] = forms.ModelChoiceField(queryset=Subject.objects.none())
                    
class AddSubject(forms.ModelForm):
    subjectName = forms.CharField(label='Subject Name', widget=forms.TextInput())
    description = forms.CharField(label='Description', widget = forms.Textarea())
    # org = forms.CharField(label='Organization', widget=forms.Select(choices=))