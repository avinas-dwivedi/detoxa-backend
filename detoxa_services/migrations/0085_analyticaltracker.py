# Generated by Django 3.2.5 on 2022-03-26 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('detoxa_services', '0084_organizations_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalyticalTracker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_answer', models.JSONField(max_length=250)),
                ('test_type', models.CharField(max_length=100, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('child', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='analytical_tracker_child', to='detoxa_services.users')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='detoxa_services.users')),
            ],
            options={
                'db_table': 'analytical_tracker',
                'managed': True,
            },
        ),
    ]
