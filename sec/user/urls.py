from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('forgot_password/', views.ForgotPasswordWizardView.as_view(), name='forgot_password'),
]
