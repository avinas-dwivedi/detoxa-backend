# Generated by Django 3.2.5 on 2021-12-31 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detoxa_services', '0046_auto_20211231_1708'),
    ]

    operations = [
        migrations.AddField(
            model_name='handeyetracker',
            name='light_on_time',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='handeyetracker',
            name='reaction_time',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
