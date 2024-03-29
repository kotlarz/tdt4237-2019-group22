# Generated by Django 2.0.6 on 2019-03-17 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('projects', '0001_initial'),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payer', to='user.Profile'),
        ),
        migrations.AddField(
            model_name='payment',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='user.Profile'),
        ),
        migrations.AddField(
            model_name='payment',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Task'),
        ),
    ]
