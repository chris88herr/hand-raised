from ast import Sub
from tkinter import CASCADE
from turtle import ondrag
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_professor = models.BooleanField(default=False)
    userType = models.CharField(max_length=10, default='None')
    
    def __str__(self) -> str:
        return f'\nname: {self.username}\nemail:{self.email}\nis_student:{self.is_student}\nis_professor:{self.is_professor}'

class Organization(models.Model):
    name = models.CharField(max_length=80)
    address = models.CharField(max_length=150)
    main_owner = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.name 

class Subject(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=150)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    organizations = models.ManyToManyField(Organization)
    subjects = models.ManyToManyField(Subject)
    # courses = models.ForeignKey(Course, on_delete=models.CASCADE)
    
class Course(models.Model):
    courseId = models.CharField(max_length=8)
    course_unique_id = models.CharField(max_length=15)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    schedule = models.CharField(max_length=30)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return "%s\r%s"  % (self.courseId, self.schedule)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    join_date = models.DateField( default=datetime.date.today)
    courses = models.ManyToManyField(Course)
    participation_score = models.IntegerField(default=0)

class Question(models.Model):
    question_title = models.CharField(max_length=40)
    question_text = models.CharField(max_length=600)
    author_by = models.ForeignKey(Student, on_delete=models.CASCADE)
    created_date = models.DateField(default= datetime.date.today)
    times_viewed = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

class QuestionComment(models.Model):
    comment_text =  models.CharField(max_length=500)
    author = models.ForeignKey(Student, on_delete=models.CASCADE)
    date_posted = models.DateField(default=datetime.date.today)
    score = models.IntegerField(default=0)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    

class Tag(models.Model):
    name = models.CharField(max_length=15)
    description = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question)

class Answer(models.Model):
    answer_text = models.CharField(max_length=500)
    author_by = models.ForeignKey(Student, on_delete=models.CASCADE)
    posted_date = models.DateField(default=datetime.date.today)
    approval_professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

class AnswerComment(models.Model):
    comment_text =  models.CharField(max_length=500)
    author = models.ForeignKey(Student ,on_delete=models.CASCADE )
    date_posted = models.DateField(default=datetime.date.today)
    score = models.IntegerField(default=0)
    answer = models.ForeignKey(Answer,on_delete=models.CASCADE)
    