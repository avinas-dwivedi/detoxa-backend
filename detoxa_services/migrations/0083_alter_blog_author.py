# Generated by Django 3.2.5 on 2022-03-05 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detoxa_services', '0082_alter_blog_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='author',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
