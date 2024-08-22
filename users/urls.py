from django.contrib import admin
from django.urls import path

from users import views

urlpatterns = [

    path('logout/', views.logout_page, name='logout_page'),
    path('login/', views.LoginPage.as_view(), name='login_page'),
    path('register/', views.RegisterPage.as_view(), name='register_page'),
    path('send-email/', views.SendingEmail.as_view(), name='sending_email')
]
