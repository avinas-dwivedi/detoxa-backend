# Generated by Django 3.2.5 on 2021-12-02 14:35

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('detoxa_services', '0003_userreport'),
    ]

    operations = [
        migrations.CreateModel(
            name='Speciality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='userreport',
            name='age',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userreport',
            name='bmi',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='userreport',
            name='child_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='detoxa_services.users'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userreport',
            name='description',
            field=models.TextField(default='description'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userreport',
            name='gender',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AddField(
            model_name='userreport',
            name='height',
            field=models.IntegerField(default=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userreport',
            name='is_downloaded',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userreport',
            name='report',
            field=models.FileField(default=1, upload_to='media'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userreport',
            name='report_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userreport',
            name='weight',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userreport',
            name='parent_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_user', to='detoxa_services.users'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='speciality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='detoxa_services.speciality'),
        ),
    ]
