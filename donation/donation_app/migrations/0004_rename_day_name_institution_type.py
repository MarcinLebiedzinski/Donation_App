# Generated by Django 4.2 on 2023-04-15 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donation_app', '0003_donation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='institution',
            old_name='day_name',
            new_name='type',
        ),
    ]
