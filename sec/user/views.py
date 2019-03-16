from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.backends.cache import SessionStore
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView
import logging
import datetime
from django.contrib.auth.signals import user_login_failed
import axes

logging.basicConfig(filename='log.txt', level=logging.WARNING)
log = logging.getLogger()

from .forms import SignUpForm, LoginForm


class IndexView(TemplateView):
    template_name = "sec/base.html"


def custom_logout(request):
    request.session = SessionStore()
    logout(request)
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
    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"]
        )
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, "Provide a valid username and/or password")

            # Unable to log failed logins axes, this is used instead.
            username = form.cleaned_data["username"]
            current_datetime = datetime.datetime.now()
            log.warning("{current_datetime}: Login failed for user: {username}".format(
                current_datetime=str(current_datetime),
                username=username))
            user_login_failed.send(sender=User,
                                   request=self.request,
                                   credentials={'username': form.cleaned_data.get('username')})
            #TODO: User is not informed s/he has been locked out unless visiting /admin. Show lockout-page.
            return super().form_invalid(form)

class SignupView(CreateView):
    form_class = SignUpForm
    template_name = "user/signup.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        # TODO: Implement zxcvbn? https://blogs.dropbox.com/tech/2012/04/zxcvbn-realistic-password-strength-estimation/
        user = form.save()
        user.profile.company = form.cleaned_data.get("company")
        user.profile.categories.add(*form.cleaned_data["categories"])
        user.save()
        login(self.request, user)

        return HttpResponseRedirect(self.success_url)
