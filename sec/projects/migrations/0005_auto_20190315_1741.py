# Generated by Django 2.0.6 on 2019-03-15 17:41

from django.db import migrations
import private_storage.fields
import private_storage.storage.files
import projects.models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20181203_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='file',
            field=private_storage.fields.PrivateFileField(storage=private_storage.storage.files.PrivateFileSystemStorage(), upload_to=projects.models.directory_path),
        ),
        migrations.AlterField(
            model_name='taskfile',
            name='file',
            field=private_storage.fields.PrivateFileField(storage=projects.models.OverwriteStorage(), upload_to=projects.models.directory_path),
        ),
    ]
