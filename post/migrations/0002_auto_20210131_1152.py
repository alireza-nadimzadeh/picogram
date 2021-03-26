# Generated by Django 2.1.11 on 2021-01-31 08:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(default=0, related_name='post_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
