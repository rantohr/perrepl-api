# Generated by Django 4.2.6 on 2023-11-26 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itineraries', '0011_alter_itinerary_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='itinerary',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]