from django.contrib import admin
from django.urls import path
from home import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("",views.index,name='index'),
    path("signup/",views.handleSignup,name='handlesignup'),
    path("login/",views.loginUser,name='login'),
    path("services/",views.services,name='services'),
    path("contact/",views.contact,name='contact'),
    path("logout/",views.logoutuser,name='logout'),
    path("password_reset/", views.password_reset_request, name="password_reset"),
    path("password/",auth_views.PasswordChangeView.as_view(template_name='password/change-password.html')),
    path("accounts/login",views.loginUser,name='login'),
    path("password_change/done/",auth_views.PasswordChangeDoneView.as_view(template_name='password/password_change_done.html')),
    
]
