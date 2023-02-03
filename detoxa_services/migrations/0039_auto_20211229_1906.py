# Generated by Django 3.2.5 on 2021-12-29 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detoxa_services', '0038_organizations'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='organizations',
            name='type',
            field=models.CharField(choices=[('School', 'School'), ('Society', 'Society'), ('Company', 'Company')], max_length=256),
        ),
    ]