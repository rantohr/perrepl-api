# Generated by Django 4.2.6 on 2023-11-26 18:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0002_rename_location_hotel_locations'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='hotel',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]