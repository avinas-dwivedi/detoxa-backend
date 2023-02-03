# Generated by Django 3.2.5 on 2022-01-27 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('detoxa_services', '0060_hospitaluser'),
    ]

    operations = [
        migrations.CreateModel(
            name='MotorSkillTracker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('child_user', models.ForeignKey(db_column='child_user_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fk_motor_skill_child_user', to='detoxa_services.users')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='detoxa_services.users')),
            ],
        ),
        migrations.CreateModel(
            name='MotorSkillTrackerSectionAnswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_name', models.CharField(choices=[('Reading', 'Reading'), ('Spelling and Writing', 'Spelling and Writing'), ('Math & Logic', 'Math & Logic'), ('Emotion & Self-Control', 'Emotion & Self-Control'), ('Listening', 'Listening'), ('Attention', 'Attention')], max_length=50)),
                ('answer', models.IntegerField(choices=[('5', '5'), ('4', '4'), ('3', '3'), ('2', '4'), ('1', '5')], default='5')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('motor_skill_tracker', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fk_motor_skill_tracker_id', to='detoxa_services.motorskilltracker')),
            ],
        ),
    ]
