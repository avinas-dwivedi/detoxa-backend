# Generated by Django 3.2.5 on 2022-03-19 13:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('detoxa_services', '0083_alter_blog_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizations',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 3, 19, 13, 50, 30, 616723, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
