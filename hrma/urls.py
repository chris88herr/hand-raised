from django.urls import path

from . import views

app_name = 'hrma'
urlpatterns = [
    path('home', views.home, name='home'),
    path('login', views.login, name='login'),
    path('signup', views.SignUpView.as_view(), name='signup')
]