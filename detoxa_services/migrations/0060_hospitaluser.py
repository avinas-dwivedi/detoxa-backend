# Generated by Django 3.2.5 on 2022-01-16 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('detoxa_services', '0059_rename_report_type_usereyesightreport_report_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='HospitalUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='detoxa_services.hospital')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='detoxa_services.users')),
            ],
            options={
                'db_table': 'hospital_user',
                'managed': True,
            },
        ),
    ]
