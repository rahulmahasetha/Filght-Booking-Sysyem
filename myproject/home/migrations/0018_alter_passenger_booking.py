# Generated by Django 5.1.7 on 2025-04-05 13:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_remove_booking_num_passengers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passenger',
            name='booking',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='passengers_booking', to='home.booking'),
        ),
    ]
