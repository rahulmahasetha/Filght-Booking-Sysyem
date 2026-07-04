from django.db import migrations, models
import decimal


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0031_remove_flight_baggage_allowance'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='fare_type',
            field=models.CharField(default='NORMAL', max_length=10, choices=[('NORMAL', 'Normal'), ('STUDENT', 'Student')]),
            preserve_default=False,
        ),
    ]
