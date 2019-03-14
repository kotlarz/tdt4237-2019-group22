from axes.decorators import axes_dispatch
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.backends.cache import SessionStore
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, CreateView, FormView
from user.models import SecurityQuestionInter
from .forms import SignUpForm, LoginForm


class IndexView(TemplateView):
    template_name = "sec/base.html"


def custom_logout(request):
    logout(request)
    request.session = SessionStore()
    return HttpResponseRedirect(reverse_lazy("home"))


@method_decorator(axes_dispatch, name='dispatch')
class LoginView(FormView):
    form_class = LoginForm
    template_name = "user/login.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = authenticate(
            request=self.request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"]
        )
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, "Provide a valid username and/or password")
            return super().form_invalid(form)


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
