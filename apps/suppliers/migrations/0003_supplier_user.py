# Generated by Django 4.2.6 on 2023-11-12 14:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('suppliers', '0002_rename_contact_supplier_contacts'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='user',
            field=models.ForeignKey(help_text='Authenticated Operator Tour', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]