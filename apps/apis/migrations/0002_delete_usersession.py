# Generated by Django 4.2.6 on 2023-12-10 18:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserSession',
        ),
    ]