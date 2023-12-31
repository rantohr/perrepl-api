# Generated by Django 4.2.6 on 2023-11-01 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_order_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_status', models.CharField(choices=[('CONFIRMED', 'Confirmed'), ('IN PROGRESS', 'In progress')], max_length=50, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
            ],
        ),
    ]
