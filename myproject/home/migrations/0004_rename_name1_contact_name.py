# Generated by Django 5.1.7 on 2025-03-17 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_rename_name_contact_name1'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='name1',
            new_name='name',
        ),
    ]
