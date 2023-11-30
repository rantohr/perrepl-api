# Generated by Django 4.2.6 on 2023-11-29 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0004_alter_supplier_name'),
        ('activities', '0006_alter_activity_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(choices=[('USD', 'USD'), ('EUR', 'EUR')], default='EUR', max_length=10)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='activities.activity')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='suppliers.supplier')),
            ],
        ),
    ]