# Generated by Django 4.2.6 on 2023-11-21 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_alter_order_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_creator',
        ),
    ]
