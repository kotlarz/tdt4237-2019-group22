from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('reset_password', views.ResetPasswordView.as_view(), name='reset_password'),
    path('forgot_password/', views.ForgotPasswordWizardView.as_view(), name='forgot_password'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.activate, name='activate')
]
