from django.urls import path

from . import views

app_name = 'hrma'
urlpatterns = [
    path('professorDashboard', views.professorDashboard, name='professorDashboard'),
    path('studentDashboard', views.studentDasboard, name='studentDashboard'),
    path('accounts/login/', views.login, name='login'),
    path('signup', views.SignUpView.as_view(), name='signup'),
    path('home', views.home, name='home'),

]