from django.contrib.auth.hashers import MD5PasswordHasher


class CustomMD5PasswordHasher(MD5PasswordHasher):

    def salt(self):
        # FIXME: Insecure Password Hashing - Static salt (OTG-CRYPST-004?)
        # TODO: https://docs.djangoproject.com/en/2.1/topics/auth/passwords/
        # TODO: Use PBKDF2 instead.
        """
        The password hashing algorithm used on the server is severely insecure. It
        is both using MD5 and a static salt.
        """
        return "tdt4237"
