# Generated by Django 4.2.6 on 2023-11-21 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travelers', '0009_alter_traveler_email_alter_traveler_first_name_and_more'),
        ('orders', '0008_remove_order_order_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_creator',
            field=models.ManyToManyField(to='travelers.traveler'),
        ),
    ]
