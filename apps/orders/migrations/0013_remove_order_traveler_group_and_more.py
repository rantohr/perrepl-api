# Generated by Django 4.2.6 on 2023-11-21 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travelers', '0010_alter_traveler_lead_traveler'),
        ('orders', '0012_alter_order_order_creator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='traveler_group',
        ),
        migrations.AlterField(
            model_name='order',
            name='order_creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders_created', to='travelers.traveler'),
        ),
    ]
