from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from projects.models import ProjectCategory


class SignUpForm(UserCreationForm):
    company = forms.CharField(max_length=30, required=False, help_text='Here you can add your company.')
    phone_number = forms.CharField(max_length=50)

    street_address = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)
    postal_code = forms.CharField(max_length=50)
    country = forms.CharField(max_length=50)

    email = forms.EmailField(max_length=254, help_text='Inform a valid email address.')
    categories = forms.ModelMultipleChoiceField(queryset=ProjectCategory.objects.all(),
                                                help_text='Hold down "Control", or "Command" on a Mac, to select more than one.',
                                                required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'categories', 'company', 'email', 'password1', 'password2',
                  'phone_number', 'street_address', 'city', 'state', 'postal_code', 'country')


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    # TODO: Implement zxcvbn? https://blogs.dropbox.com/tech/2012/04/zxcvbn-realistic-password-strength-estimation/
    password = forms.CharField(required=True, widget=forms.TextInput(attrs={"type": "password"}))

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        user = User.objects.filter(username=username).first()



        if user.temporary_password is not None:
            if not check_password(password=password, encoded=user.temporary_password):
                # Raise ValidationError





class ResetPasswordForm(forms.Form):
    temp_password = forms.PasswordInput(required=True)
    new_password_1 = forms.PasswordInput(required=True)
    new_password_2 = forms.PasswordInput(required=True)

    def validate_temp_password(self):
        #TODO: Check if temp password is correct

        temp_password = self.cleaned_data.get("temp_password")

        if not User.objects.filter(temp_password=temp_password) == self.temp_password:
            raise ValidationError("The entered temporary password is wrong")
        return True

    def cross_check_new_passwords(self):
        if not self.new_password_1 == self.new_password_2:
            raise ValidationError("The passwords must match")
        return True
