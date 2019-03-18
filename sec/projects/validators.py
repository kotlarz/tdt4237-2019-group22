import magic
from django.core.exceptions import ValidationError

from sec import settings


def validate_file_extension(file):
    mime = magic.from_buffer(file.read(1024), mime=True)
    if mime not in settings.MIMETYPES:
        raise ValidationError('{0} is of filetype {1} which is not an acceptable file type'.format(file, mime))