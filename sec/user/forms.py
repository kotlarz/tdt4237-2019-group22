from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList

from projects.models import ProjectCategory
from user.models import SecurityQuestion


class SecurityQuestionChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.question


SECURITY_UNIQUE_VALIDATION_ERROR_MESSAGE = "Security questions need to be unique"


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

    security_question_1 = SecurityQuestionChoiceField(queryset=SecurityQuestion.objects.all(),
                                                      help_text='Select your first Security Question')
    security_question_1_answer = forms.CharField(max_length=250)

    security_question_2 = SecurityQuestionChoiceField(queryset=SecurityQuestion.objects.all(),
                                                      help_text='Select your second Security Question')
    security_question_2_answer = forms.CharField(max_length=250)

    security_question_3 = SecurityQuestionChoiceField(queryset=SecurityQuestion.objects.all(),
                                                      help_text='Select your third Security Question')
    security_question_3_answer = forms.CharField(max_length=250)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'categories', 'company', 'email',
                  'password1', 'password2', 'security_question_1', 'security_question_1_answer',
                  'security_question_2', 'security_question_2_answer', 'security_question_3',
                  'security_question_3_answer', 'phone_number', 'street_address', 'city', 'state',
                  'postal_code', 'country')

    def clean_security_question_2(self):
        security_question_1 = self.cleaned_data.get("security_question_1")
        security_question_2 = self.cleaned_data.get("security_question_2")
        security_question_3 = self.cleaned_data.get("security_question_3")

        if security_question_2 in [security_question_1, security_question_3]:
            raise ValidationError(SECURITY_UNIQUE_VALIDATION_ERROR_MESSAGE)

        return security_question_2

    def clean_security_question_3(self):
        security_question_1 = self.cleaned_data.get("security_question_1")
        security_question_2 = self.cleaned_data.get("security_question_2")
        security_question_3 = self.cleaned_data.get("security_question_3")

        if security_question_3 in [security_question_1, security_question_2]:
            raise ValidationError(SECURITY_UNIQUE_VALIDATION_ERROR_MESSAGE)

        return security_question_3


class LoginForm(forms.Form):
    username = forms.CharField(required=True)

    # TODO: Implement zxcvbn? https://blogs.dropbox.com/tech/2012/04/zxcvbn-realistic-password-strength-estimation/
    password = forms.CharField(required=True, widget=forms.TextInput(attrs={"type": "password"}))
