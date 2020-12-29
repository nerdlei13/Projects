# Generated by Django 3.1.1 on 2020-11-12 05:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ShowUsers',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('joined', models.DateTimeField(auto_now=True)),
                ('superuser', models.CharField(max_length=200)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SearchHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('subreddit', models.CharField(max_length=200)),
                ('keyword', models.CharField(max_length=200)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AdvancedSearchHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('subreddit', models.CharField(max_length=200)),
                ('word_in_title', models.CharField(max_length=200)),
                ('word_not_in_title', models.CharField(max_length=200)),
                ('word_in_comment', models.CharField(max_length=200)),
                ('word_not_in_comment', models.CharField(max_length=200)),
                ('search_within', models.CharField(max_length=200)),
                ('search_limit', models.CharField(max_length=200)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
