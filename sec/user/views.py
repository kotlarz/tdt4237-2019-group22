from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.contrib.sessions.backends.cache import SessionStore
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView

from user.models import SecurityQuestionInter

from user.models import AppUser
from .forms import SignUpForm, LoginForm, ForgotPasswordForm, ResetPasswordForm


class IndexView(TemplateView):
    template_name = "sec/base.html"


# FIXME: No Session Expiration - Invalidate session on logout
"""
Sessions have virtually no expiration (~70 years).
Neither is the session invalidated on logout.
"""
def logout(request):
    request.session = SessionStore()
    return HttpResponseRedirect(reverse_lazy("home"))


# FIXME: No Session Renewal - Rewnew on login
"""
Sessions are not renewed on login. In addition, the same session id is shared
between all sessions for a single user. This means that, together with no session
expiration, if an attacker gains access to the session of a user, the attacker
will have permanent access to the user
"""
class LoginView(FormView):
    form_class = LoginForm
    template_name = "user/login.html"
    success_url = reverse_lazy("home")

    # FIXME: No Login Throttling/No Lockout Mechanism
    # TODO: Lookup django-axes or django-ratelimit.
    """
    Neither login throttling, nor a lockout mechanism is implemented.
    Making it very simple for an attacker to perform brute force attacks
    on the login page.
    """
    # FIXME: Insufficient logging and monitoring (Top 10-2017 A10):
    """
    Exploitation of insufficient logging and monitoring is the bedrock of nearly
    every major incident. Attackers rely on the lack of monitoring and timely
    response to achieve their goals without being detected.
    All group should add logging of failed login attempts.
    """
    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=username, password=password)
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
                profile=user.profile,
                security_question=security_question,
                answer=security_question_answer
            )
        user.profile.company = form.cleaned_data.get("company")
        user.profile.categories.add(*form.cleaned_data["categories"])
        user.save()
        login(self.request, user)

        return HttpResponseRedirect(self.success_url)


class ResetPasswordView(FormView):
    form_class = ResetPasswordForm
    template_name = "user/reset_password.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        username = self.request.session["username"]
        temporary_password = form.cleaned_data.get("temporary_password")
        if AppUser.objects.filter(username=username) == AppUser.username and AppUser.objects.filter(temporary_password=temporary_password) == AppUser.temporary_password:
            AppUser.set_password(self, form.cleaned_data.get("new_password_2"))
            AppUser.temporary_password = None
            AppUser.save(self)
            return HttpResponseRedirect(self.success_url)
        raise ValidationError("The entered temporary password is wrong")


class ForgotPasswordView(FormView):
    form_class = ForgotPasswordForm
    template_name = "user/forgot_password.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        # TODO: add logic
        return HttpResponseRedirect(self.success_url)
