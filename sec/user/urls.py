from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('reset_password', views.ResetPasswordView.as_view(), name='reset_password'),
    path('forgot_password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
]
