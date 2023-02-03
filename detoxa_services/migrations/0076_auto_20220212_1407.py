# Generated by Django 3.2.5 on 2022-02-12 14:07

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('detoxa_services', '0075_auto_20220212_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='eyesighttracker',
            name='child',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='eye_sight_child', to='detoxa_services.users'),
        ),
        migrations.AddField(
            model_name='eyesighttracker',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eyesighttracker',
            name='eye_side',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eyesighttracker',
            name='test_name_answer',
            field=models.JSONField(default='', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eyesighttracker',
            name='test_type',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='eyesighttracker',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='eyesighttracker',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='detoxa_services.users'),
        ),
    ]
