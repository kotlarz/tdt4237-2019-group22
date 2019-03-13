from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.sessions.backends.cache import SessionStore
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string


from .tokens import account_activation_token
from .forms import SignUpForm, LoginForm


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
        try:
            password = make_password(form.cleaned_data["password"])
            # FIXME: SQL Injection - Rewrite to use proper model lookup
            """
            The login page is vulnerable to SQL injections.
            An attacker may for example login to user with username “admin”
            by entering admin’-- in the username field.
            """
            user = User.objects.raw("SELECT * FROM auth_user WHERE username='" + form.cleaned_data[
                "username"] + "' AND password='" + password + "';")[0]
            login(self.request, user)
            return super().form_valid(form)
        except IndexError:
            form.add_error(None, "Provide a valid username and/or password")
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
        user.is_active = False
        user.save()

        message = render_to_string('user/acc_active_email.html', {
            'user': user,
            'domain': "127.0.0.1:8000",
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': account_activation_token.make_token(user),
        })

        to_email = form.cleaned_data.get('email')
        # email = EmailMessage(
        #     "Confirm email", message, to=[to_email]
        # )
        # email.send()

        send_mail(
            'Subject here',
            'Here is the message.',
            'netland.ingvild@gmail.com',
            ['netland.ingvild@gmail.com'],
            fail_silently=False,
        )

        return HttpResponse('Please confirm your email address to complete the registration')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print(uid)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
