# Generated by Django 4.2.6 on 2023-12-11 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_managers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_logged_in',
        ),
    ]