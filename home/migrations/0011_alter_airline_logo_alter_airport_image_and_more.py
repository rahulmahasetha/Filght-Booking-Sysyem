# Generated by Django 5.1.7 on 2025-04-05 07:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_populate_booking_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airline',
            name='logo',
            field=models.ImageField(blank=True, default='default_airline.jpg', null=True, upload_to='airlines/'),
        ),
        migrations.AlterField(
            model_name='airport',
            name='image',
            field=models.ImageField(blank=True, default='default_airport.jpg', null=True, upload_to='airports/'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(max_length=100),
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.CharField(max_length=15, validators=[django.core.validators.RegexValidator('^\\+?\\d{10,15}$', 'Invalid phone number format.')]),
        ),
        migrations.AlterField(
            model_name='contact',
            name='pincode',
            field=models.CharField(max_length=6, validators=[django.core.validators.RegexValidator('^\\d{6}$', 'Invalid pincode format.')]),
        ),
    ]
