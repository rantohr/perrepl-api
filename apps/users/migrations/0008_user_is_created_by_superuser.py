# Generated by Django 4.2.6 on 2023-12-11 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_user_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_created_by_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
