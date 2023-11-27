# Generated by Django 4.2.6 on 2023-11-22 18:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_alter_orderstatus_order'),
        ('travelers', '0011_alter_traveler_gender'),
        ('itineraries', '0005_alter_itinerarysegment_end_location_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='itinerary',
            name='clients',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='itineraries', to='travelers.traveler'),
        ),
        migrations.AddField(
            model_name='itinerary',
            name='orders',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_itineraries', to='orders.order'),
        ),
    ]