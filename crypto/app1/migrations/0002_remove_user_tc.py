# Generated by Django 4.1 on 2022-08-26 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='tc',
        ),
    ]
