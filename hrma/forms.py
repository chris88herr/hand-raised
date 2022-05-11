from ctypes import windll
from lib2to3.pgen2.token import LBRACE
from turtle import textinput
from django.contrib.auth.forms import UserCreationForm
from pkg_resources import require
from hrma.utlis.db import getSubjectsQuerySetListFromOrg,getSubjectsQuerySetListFromCourse
from hrma.models import Subject
from hrma.models import User
from django import forms
from hrma.models import Student, Professor, Organization, Course
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

#----------------------------------------PROFESSOR FORMS -----------------------------------------------
class AddOrganizationToProfessor(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AddOrganizationToProfessor, self).__init__(*args, **kwargs)
        self._build_fields()

    def _build_fields(self):
        orgs = Organization.objects.all()
        self.fields['organizations'] = forms.ModelChoiceField(queryset=orgs)

class AddSubjectToProfessor(forms.Form):
    def __init__(self, *args, **kwargs):
        print(kwargs)
        self.user = kwargs.pop("user")
        super(AddSubjectToProfessor, self).__init__(*args, **kwargs)
        self._build_fields()

    def _build_fields(self):
        self.professor = Professor.objects.filter(pk=self.user).first()
        print(f'professor {self.professor}')
        if self.professor.organizations:
            orgs = self.professor.organizations.all()
            self.fields['organizations'] = forms.ModelChoiceField(queryset=orgs)
            subjectsList = getSubjectsQuerySetListFromOrg(orgs)
            if len(subjectsList)>0:
                subjects = QuerySet.union(*subjectsList)
                self.fields['subjects'] = forms.ModelChoiceField(queryset=subjects)
            else:
                self.fields['subjects'] = forms.ModelChoiceField(queryset=Subject.objects.none())

class AddCourseToProfessor(AddSubjectToProfessor):
    def __init__(self, *args, **kwargs):
        print('init....')
        super(AddCourseToProfessor, self).__init__(*args, **kwargs)
        print('init.... finished')
        
    def _build_fields(self):
        super (AddCourseToProfessor,self)._build_fields()
        self.fields['course'] = forms.CharField(widget=forms.TextInput(attrs={'label':'course'}))
        
#----------------------------------------STUDENT FORMS -----------------------------------------------

class AddOrgToStudentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        print('add org form init')
        super(AddOrgToStudentForm, self).__init__(*args, *kwargs)
        self._build_fields()
        print('add org form finish')
    def _build_fields(self):
        orgs = Organization.objects.all()
        self.fields['organization'] = forms.ModelChoiceField(queryset=orgs)

class AddCourseToStudentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AddCourseToStudentForm, self).__init__(*args, **kwargs)
        self._build_fields()

    def _build_fields(self):
        student = Student.objects.filter(pk=self.user).first()
        student_orgs = student.organizations.all()
        org_courses =  Course.objects.filter(organization__in= list(student_orgs))
        print(f'student orgs {type(student_orgs)} {student_orgs}')
        print(f'orgs_classes {type(org_courses)} {org_courses}')
        self.fields['student_orgs'] = forms.ModelChoiceField(queryset=student_orgs)
        self.fields['org_courses'] = forms.ModelChoiceField(queryset=org_courses)

class PostQuestionForm(forms.Form):
    def __init__(self, *args, **kwargs) -> None:
        super(PostQuestionForm, self).__init__()
        self._build_fields()

    def _build_fields(self):
        self.fields['questionTitle'] = forms.CharField(widget=forms.TextInput(attrs={'label', 'Question Title'}))
        self.fields['questionBody'] = forms.CharField(widget=forms.Textarea(attrs={'label', 'Question details'}))

class PostAnswerForm(forms.Form):
    def __init__(self, *args, **kwargs) -> None:
        super(PostAnswerForm, self).__init__()
        self._build_fields()

    def _build_fields(self):
        self.fields['answer'] = forms.CharField(widget=forms.TextInput())

class PostAnswerCommentForm(forms.Form):
    def __init__(self, *args, **kwargs) -> None:
        super(PostAnswerCommentForm, self).__init__()
        self._build_fields()

    def _build_fields(self):
        self.fields['answerComment'] = forms.CharField(widget=forms.TextInput())

class PostQuestionComment(forms.Form):
    def __init__(self, *args, **kwargs) -> None:
        super(PostQuestionComment, self).__init__()
        self._build_fields()

    def _build_fields(self):
        self.fields['questionComment'] = forms.CharField(widget=forms.TextInput())



#----------------------------------------OTHER FORMS -----------------------------------------------

class AddSubject(forms.ModelForm):
    subjectName = forms.CharField(label='Subject Name', widget=forms.TextInput())
    description = forms.CharField(label='Description', widget = forms.Textarea())
    # org = forms.CharField(label='Organization', widget=forms.Select(choices=))