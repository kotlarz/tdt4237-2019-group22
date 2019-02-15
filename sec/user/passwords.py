from django.contrib.auth.hashers import MD5PasswordHasher


class CustomMD5PasswordHasher(MD5PasswordHasher):

    def salt(self):
        # FIXME: Static salt (OTG-CRYPST-004?)
        return "tdt4237"
