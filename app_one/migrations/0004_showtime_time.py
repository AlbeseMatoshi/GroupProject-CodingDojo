# Generated by Django 3.0.8 on 2020-07-30 21:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_one', '0003_delete_events'),
    ]

    operations = [
        migrations.AddField(
            model_name='showtime',
            name='time',
            field=models.TimeField(default=datetime.datetime.now),
        ),
    ]