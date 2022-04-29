from django.contrib.auth.forms import UserCreationForm
from hrma.models import User
from django import forms
from hrma.models import Student, Professor

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