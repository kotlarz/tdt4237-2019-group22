import django
import sys
import platform


# FIXME: Security Misconfiguration - Remove, server2 header, etc. in production
class InformationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response[
            "Server2"] = f"Django/{django.get_version()} Python/{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.serial} {platform.system()}/{platform.release()}"
        return response

