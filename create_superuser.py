from django.contrib.auth import get_user_model
from django.conf import settings

password = settings.DEFAULT_ADMIN_PASSWORD

User = get_user_model()
admin = User.objects.filter(username="admin").first()
if admin is None:
    User.objects.create_superuser("admin", "admin@localhost", password)
else:
    admin.set_password(password)
    admin.save()
