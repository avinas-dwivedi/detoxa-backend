# Generated by Django 3.2.5 on 2023-01-03 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detoxa_services', '0123_blog_updated'),
    ]

    operations = [
        migrations.CreateModel(
            name='Animals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('animal_type', models.CharField(max_length=50)),
                ('animal_name', models.CharField(max_length=300)),
                ('audio_1_url', models.CharField(blank=True, max_length=500, null=True)),
                ('audio_2_url', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_name', models.CharField(max_length=100)),
                ('audio_1_url', models.CharField(blank=True, max_length=500, null=True)),
                ('audio_2_url', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CountryStates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state_name', models.CharField(max_length=300)),
                ('state_code', models.CharField(max_length=100)),
                ('state_capital', models.CharField(max_length=300)),
                ('audio_1_url', models.CharField(max_length=500)),
                ('audio_2_url', models.CharField(blank=True, max_length=500, null=True)),
                ('audio_3_url', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profession_name', models.CharField(max_length=100)),
                ('audio_1_url', models.CharField(blank=True, max_length=500, null=True)),
                ('audio_2_url', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SolorSystem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solor_name', models.CharField(max_length=100)),
                ('audio_1_url', models.CharField(blank=True, max_length=500, null=True)),
                ('audio_2_url', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_name', models.CharField(max_length=100)),
                ('audio_1_url', models.CharField(blank=True, max_length=500, null=True)),
                ('audio_2_url', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='doctors',
            name='days',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='therapist',
            name='days',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='coupon_code',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]