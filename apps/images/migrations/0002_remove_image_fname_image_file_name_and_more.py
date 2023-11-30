# Generated by Django 4.2.6 on 2023-11-30 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='fname',
        ),
        migrations.AddField(
            model_name='image',
            name='file_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='folder_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
