# Generated by Django 3.2.5 on 2021-12-20 05:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('detoxa_services', '0026_auto_20211219_1242'),
    ]

    operations = [
        migrations.AddField(
            model_name='learnabilitytracker',
            name='child_user',
            field=models.ForeignKey(db_column='child_user_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fk_learnablity_child_user', to='detoxa_services.users'),
        ),
    ]