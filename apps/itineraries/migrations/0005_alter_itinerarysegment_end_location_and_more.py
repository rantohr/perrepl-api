# Generated by Django 4.2.6 on 2023-11-21 18:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mada_countries', '0003_geographicalcoordinate_remove_madacountry_latitude_and_more'),
        ('itineraries', '0004_itinerary_user_itinerarysegment_arrival_time_utc_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itinerarysegment',
            name='end_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='end_locations_set', to='mada_countries.madacountry'),
        ),
        migrations.AlterField(
            model_name='itinerarysegment',
            name='start_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='start_locations_set', to='mada_countries.madacountry'),
        ),
    ]