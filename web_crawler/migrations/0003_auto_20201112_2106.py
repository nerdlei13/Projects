# Generated by Django 3.1.1 on 2020-11-13 05:06

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web_crawler', '0002_auto_20201112_0002'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AuthUser',
            new_name='ShowUsers',
        ),
    ]