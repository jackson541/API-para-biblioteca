# Generated by Django 3.0.5 on 2020-04-12 17:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_auto_20200412_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='date_register',
            field=models.DateField(default=datetime.datetime(2020, 4, 12, 17, 44, 13, 486845, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='loan',
            name='loan_date',
            field=models.DateField(default=datetime.datetime(2020, 4, 12, 17, 44, 13, 487845, tzinfo=utc)),
        ),
    ]