# Generated by Django 4.2.6 on 2023-11-29 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0008_alter_hotel_image_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='image_name',
            field=models.CharField(default='<function uuid4 at 0x7f377ab569e0>', max_length=255, unique=True),
        ),
    ]
