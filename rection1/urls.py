from django.urls import path
from . import views

urlpatterns=[
    path('login/', views.login, name='login'),
    path('loginConf/', views.loginConf, name='loginConf'),
    path('signup/', views.signUp, name='signup'),
    path('position/', views.position, name='position'),
]