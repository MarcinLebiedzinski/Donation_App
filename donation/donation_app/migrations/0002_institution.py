# Generated by Django 4.2 on 2023-04-15 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField(null=True)),
                ('day_name', models.SmallIntegerField(choices=[(-1, 'not defined'), (0, 'fundacja'), (1, 'organizacja pozarządowa'), (2, 'zbiórka lokalna')], default=0)),
                ('categories', models.ManyToManyField(to='donation_app.category')),
            ],
        ),
    ]
