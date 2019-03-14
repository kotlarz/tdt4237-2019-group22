from django.contrib.auth import user_logged_in
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# FROM: https://stackoverflow.com/questions/9763099/adding-security-questions-to-my-django-site
class SecurityQuestion(models.Model):
    class Meta:
        db_table = 'security_questions'
    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=250, null=False)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    company = models.TextField(max_length=50, blank=True)
    phone_number = models.TextField(max_length=50, blank=True)
    street_address = models.TextField(max_length=50, blank=True)
    city = models.TextField(max_length=50, blank=True)
    state = models.TextField(max_length=50, blank=True)
    postal_code = models.TextField(max_length=50, blank=True)
    country = models.TextField(max_length=50, blank=True)
    categories = models.ManyToManyField('projects.ProjectCategory', related_name='competance_categories')
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, blank=True, default=None, null=True)
    security_questions = models.ManyToManyField(SecurityQuestion, through='SecurityQuestionInter')

    def __str__(self):
        return self.user.username


class SecurityQuestionInter(models.Model):
    class Meta:
        db_table = 'security_questions_inter'

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    security_question = models.ForeignKey(SecurityQuestion, on_delete=models.CASCADE)
    answer = models.CharField(max_length=250, null=False)

    @staticmethod
    def hash_answer(answer):
        # This might be considered a bad options (lowering the string),
        # but it should be fine for security questions.
        return make_password(answer.lower())

    def is_valid_answer(self, answer):
        # This might be considered a bad options (lowering the string),
        # but it should be fine for security questions.
        return check_password(answer.lower(), self.answer)

    def save(self, *args, **kwargs):
        self.answer = SecurityQuestionInter.hash_answer(self.answer)
        super(SecurityQuestionInter, self).save(*args, **kwargs)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
