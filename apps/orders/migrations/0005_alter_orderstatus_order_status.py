# Generated by Django 4.2.6 on 2023-11-01 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_orderstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderstatus',
            name='order_status',
            field=models.CharField(choices=[('CONFIRMED', 'Confirmed'), ('IN PROGRESS', 'In progress')], default='NEW', max_length=50, null=True),
        ),
    ]
