# Generated by Django 4.2.6 on 2023-12-03 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0015_remove_hotel_images'),
        ('images', '0002_remove_image_fname_image_file_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='hotel_image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hotel_images', to='hotels.hotel'),
        ),
    ]