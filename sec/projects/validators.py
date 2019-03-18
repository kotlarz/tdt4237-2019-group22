import magic
from django.core.exceptions import ValidationError

from sec import settings


def validate_file_extension(file):
    mime = magic.from_buffer(file.read(1024), mime=True)
    if mime not in settings.MIMETYPES:
        raise ValidationError('{0} is of filetype {1} which is not an acceptable file type'.format(file, mime))

def validate_file_size(file):
    if file.size > settings.MAX_FILE_SIZE:
        raise ValidationError('File {0} is too big. File size is {1} MB, and maximum file size is {2} MB.'
                              .format(file, file.size/1000000, settings.MAX_FILE_SIZE/1000000))