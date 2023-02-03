# Generated by Django 3.2.5 on 2021-12-29 04:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('detoxa_services', '0036_auto_20211225_1236'),
    ]

    operations = [
        migrations.CreateModel(
            name='LearnalityTrackerSectionAnswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_name', models.CharField(choices=[('Reading', 'Reading'), ('Spelling and Writing', 'Spelling and Writing'), ('Math & Logic', 'Math & Logic'), ('Emotion & Self-Control', 'Emotion & Self-Control'), ('Listening', 'Listening'), ('Attention', 'Attention')], max_length=50)),
                ('answer', models.IntegerField(choices=[('5', '5'), ('4', '4'), ('3', '3'), ('2', '4'), ('1', '5')], default='5')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'learnability_tracker_section_answers',
                'managed': True,
            },
        ),
        migrations.DeleteModel(
            name='ChildTrackerGenderChoice',
        ),
        migrations.RemoveField(
            model_name='doctors',
            name='email',
        ),
        migrations.RemoveField(
            model_name='doctors',
            name='mobile',
        ),
        migrations.RemoveField(
            model_name='doctors',
            name='profile_image_extension',
        ),
        migrations.RemoveField(
            model_name='doctors',
            name='profile_image_key',
        ),
        migrations.RemoveField(
            model_name='learnabilitytracker',
            name='age',
        ),
        migrations.RemoveField(
            model_name='learnabilitytracker',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='learnabilitytracker',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='learnabilitytracker',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='learnabilitytracker',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='learnabilitytracker',
            name='section_name',
        ),
        migrations.AddField(
            model_name='doctors',
            name='doc_image',
            field=models.CharField(default='', max_length=5000),
        ),
        migrations.AddField(
            model_name='doctors',
            name='doc_image_url',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='learnalitytrackersectionanswers',
            name='learnablity_tracker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fk_learnablity_tracker_id', to='detoxa_services.learnabilitytracker'),
        ),
    ]
