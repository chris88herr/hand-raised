from django.urls import path

from . import views

app_name = 'hrma'
urlpatterns = [
    path('professorDashboard', views.ProfessorDashboard.as_view(), name='professorDashboard'),
    path('studentDashboard', views.StudentDasboard.as_view(), name='studentDashboard'),
    path('studentDashboard/courses/<str:course_id>/', views.CoursesView.as_view(), name='professorDashboard'),
    path('accounts/login/', views.login, name='login'),
    path('signup', views.SignUpView.as_view(), name='signup'),
    path('home', views.home, name='home'),

]