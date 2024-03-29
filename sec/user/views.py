from axes.decorators import axes_dispatch
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.backends.cache import SessionStore
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, CreateView, FormView
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from formtools.wizard.views import SessionWizardView
from user.models import SecurityQuestionInter, AppUser
from django.contrib import messages


from .tokens import account_activation_token
from .forms import SignUpForm, LoginForm, ForgotPasswordForm, ForgotPasswordSecurityQuestionsForm, \
    ResetPasswordForm


def custom_logout(request):
    logout(request)
    request.session = SessionStore()
    return HttpResponseRedirect(reverse_lazy("home"))


def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = AppUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, AppUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account is now activated and you can log in.')
        return HttpResponseRedirect(reverse_lazy("login"))
    else:
        user.send_activation_mail()
        return render(request, 'user/activation_expired.html')


class IndexView(TemplateView):
    template_name = "sec/base.html"


@method_decorator(axes_dispatch, name='dispatch')
class LoginView(FormView):
    form_class = LoginForm
    template_name = "user/login.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(
            request=self.request,
            username=username,
            password=password,
        )
        if user is not None:
            login(self.request, user)
            user.temporary_password = None
            user.save()
            return super(LoginView, self).form_valid(form)

        user = AppUser.objects.get(username=username)
        if user is not None \
                and user.temporary_password is not None \
                and user.check_temporary_password(raw_password=password):
            self.request.session["username"] = form.cleaned_data["username"]
            return HttpResponseRedirect(reverse_lazy("reset_password"))

        form.add_error(None, "Provide a valid username and/or password")
        return super(LoginView, self).form_invalid(form)


class SignupView(CreateView):
    form_class = SignUpForm
    template_name = "user/signup.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        # TODO: Implement zxcvbn? https://blogs.dropbox.com/tech/2012/04/zxcvbn-realistic-password-strength-estimation/
        security_question_1 = form.cleaned_data.pop("security_question_1")
        security_question_1_answer = form.cleaned_data.pop("security_question_1_answer")
        security_question_2 = form.cleaned_data.pop("security_question_2")
        security_question_2_answer = form.cleaned_data.pop("security_question_2_answer")
        security_question_3 = form.cleaned_data.pop("security_question_3")
        security_question_3_answer = form.cleaned_data.pop("security_question_3_answer")

        security_questions = [security_question_1, security_question_2, security_question_3]
        security_question_answers = [
            security_question_1_answer,
            security_question_2_answer,
            security_question_3_answer
        ]

        user = form.save()
        for i in range(len(security_questions)):
            security_question = security_questions[i]
            security_question_answer = security_question_answers[i]
            SecurityQuestionInter.objects.create(
                user=user,
                security_question=security_question,
                answer=security_question_answer
            )
        user.profile.company = form.cleaned_data.get("company")
        user.profile.categories.add(*form.cleaned_data["categories"])
        user.is_active = False
        user.save()
        user.send_activation_mail()

        return render(self.request, 'user/signup_done.html')


class ResetPasswordView(FormView):
    form_class = ResetPasswordForm
    template_name = "user/reset_password.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        username = self.request.session["username"]
        temporary_password = form.cleaned_data.get("temporary_password")
        user = AppUser.objects.get(username=username)
        if user.check_temporary_password(temporary_password):
            user.set_password(form.cleaned_data.get("new_password_2"))
            user.temporary_password = None
            user.save()
            del self.request.session['username']
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect(self.success_url)
        raise ValidationError("The entered temporary password is wrong")


class ForgotPasswordWizardView(SessionWizardView):
    form_list = [ForgotPasswordForm, ForgotPasswordSecurityQuestionsForm]
    template_name = "user/forgot_password.html"

    def done(self, form_list, **kwargs):
        email_form = list(form_list)[0]
        user = AppUser.objects.filter(email=email_form.cleaned_data['email']).first()
        temporary_password = AppUser.objects.make_random_password()
        user.set_temporary_password(temporary_password)
        user.send_temporary_password_email(temporary_password)
        return render(self.request, 'user/forgot_password_done.html')

    def get_form_kwargs(self, step=None):
        kwargs = {}
        if step == '1':
            email = self.get_cleaned_data_for_step('0')['email']
            kwargs.update({'email': email, })
        return kwargs
