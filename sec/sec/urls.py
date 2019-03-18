from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from sec import settings

# FIXME: Stored session keys in admin panel (OTG-CONFIG-005)
"""
All session keys for users are visible from the admin panel. If an attacker can get admin
access on the site, he can steal all session keys and get access to all other users. Remove
all information about sessions keys from site.
"""
# FIXME: disable /admin in prod, or maybe not?
urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('projects/', include('projects.urls')),
    path('payment/', include('payment.urls')),
]
