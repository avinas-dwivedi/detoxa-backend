# Generated by Django 3.2.5 on 2021-11-28 16:22

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'author',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('device_type', models.CharField(choices=[('web', 'Web'), ('mobile', 'Mobile')], max_length=30, null=True)),
                ('picture_url', models.TextField(null=True)),
                ('sequence_number', models.CharField(choices=[('one', 'One'), ('two', 'Two'), ('three', 'Three'), ('four', 'Four'), ('five', 'Five'), ('six', 'Six'), ('seven', 'Seven'), ('eight', 'Eight'), ('nine', 'Nine'), ('ten', 'Ten')], max_length=30, null=True)),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('page_link', models.CharField(max_length=200, null=True)),
                ('key', models.CharField(max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'banner',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('media_url', models.TextField(null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'blog_category',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ChildGenderChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ChildTrackerGenderChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=200, validators=[django.core.validators.EmailValidator])),
                ('mobile', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in the format: 919999999999 of length 11 to 14.', regex='^\\d{11,13}$')])),
                ('message', models.TextField()),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'contact_us',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='DeviceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('speciality', models.CharField(max_length=256)),
                ('degree', models.CharField(max_length=256)),
                ('image', models.CharField(blank=True, max_length=256, null=True)),
                ('experience', models.FloatField(max_length=256)),
                ('email', models.EmailField(max_length=50)),
                ('phone', models.CharField(max_length=50)),
                ('time_slots', models.CharField(max_length=256)),
                ('fees', models.FloatField(max_length=256)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'doctor',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=0)),
                ('comment', models.TextField()),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='MediaCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'media_category',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='MediaType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='MobileOTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_no', models.CharField(max_length=80, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in the format: 919999999999 of length 11 to 14.', regex='^\\d{11,13}$')])),
                ('otp', models.IntegerField()),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'mobile_otp',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Promocode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True)),
                ('discount', models.IntegerField()),
                ('is_expired', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'promocode',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SequenceNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'services',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='UserGenderChoices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150)),
                ('password', models.CharField(max_length=200, null=True)),
                ('email', models.EmailField(max_length=200, null=True, unique=True, validators=[django.core.validators.EmailValidator])),
                ('mobile', models.CharField(max_length=30, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in the format: 919999999999 of length 11 to 14.', regex='^\\d{11,13}$')])),
                ('mobile_code', models.CharField(max_length=6, null=True, validators=[django.core.validators.MinLengthValidator(6)])),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=6, null=True)),
                ('profile_pic_url', models.TextField(null=True)),
                ('key', models.CharField(max_length=255, null=True)),
                ('dob', models.DateField(null=True)),
                ('age', models.CharField(max_length=20, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_tnc_accepted', models.BooleanField(default=False)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'users',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='VaccinationData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('min_age', models.IntegerField(default=0)),
                ('max_age', models.IntegerField(default=0)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'vaccination_data',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UserChildRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active', max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('child_user', models.ForeignKey(db_column='child_user_id', on_delete=django.db.models.deletion.CASCADE, related_name='fk_child_user', to='detoxa_services.users')),
                ('parent_user', models.ForeignKey(db_column='parent_user_id', on_delete=django.db.models.deletion.CASCADE, related_name='fk_parent_user', to='detoxa_services.users')),
            ],
            options={
                'db_table': 'user_child_relation',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UserActiveTokens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_token', models.CharField(max_length=1024)),
                ('is_active', models.BooleanField(default=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(db_column='user_token_id', on_delete=django.db.models.deletion.CASCADE, to='detoxa_services.users')),
            ],
            options={
                'db_table': 'user_active_tokens',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Testimonials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=100)),
                ('picture_url', models.TextField(null=True)),
                ('testimonial', models.TextField(null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('service', models.ForeignKey(db_column='service_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fk_service_id', to='detoxa_services.services')),
            ],
            options={
                'db_table': 'testimonials',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='MyVaccinationDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Booked', 'Booked'), ('Done', 'Done'), ('OverDue', 'OverDue'), ('Upcoming', 'Upcoming'), ('Cancelled', 'Cancelled')], default='Upcoming', max_length=50)),
                ('reminder_date', models.DateField(null=True)),
                ('reminder_time', models.TimeField(null=True)),
                ('is_reminder_added', models.BooleanField(default=False)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, related_name='fk_vaccine_user_id', to='detoxa_services.users')),
                ('vaccine', models.ForeignKey(db_column='vaccine_id', on_delete=django.db.models.deletion.CASCADE, related_name='fk_vaccine_id', to='detoxa_services.vaccinationdata')),
            ],
            options={
                'db_table': 'my_vaccine_details',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('media_type', models.CharField(choices=[('image', 'image'), ('video', 'video')], max_length=20, null=True)),
                ('media_url', models.TextField(null=True)),
                ('key', models.CharField(max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(db_column='category_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fk_category_id', to='detoxa_services.mediacategory')),
            ],
            options={
                'db_table': 'media',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='LearnabilityTracker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_name', models.CharField(choices=[('Reading', 'Reading'), ('Spelling and Writing', 'Spelling and Writing'), ('Math & Logic', 'Math & Logic'), ('Emotion & Self-Control', 'Emotion & Self-Control'), ('Listening', 'Listening'), ('Attention', 'Attention')], max_length=50)),
                ('answer', models.IntegerField(choices=[('5', '5'), ('4', '4'), ('3', '3'), ('2', '4'), ('1', '5')], default='5')),
                ('first_name', models.CharField(max_length=40, null=True)),
                ('last_name', models.CharField(max_length=40, null=True)),
                ('age', models.IntegerField(default=0)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], default='Male', max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='detoxa_services.users')),
            ],
            options={
                'db_table': 'learnability_tracker',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='HandEyeTracker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_name', models.CharField(max_length=100)),
                ('test_question_answer', models.JSONField()),
                ('first_name', models.CharField(max_length=60)),
                ('last_name', models.CharField(max_length=60)),
                ('age', models.CharField(max_length=10)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], max_length=20)),
                ('average', models.FloatField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(db_column='user_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fk_user_id', to='detoxa_services.users')),
            ],
            options={
                'db_table': 'hand_eye_tracker',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='EyeSightTracker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_name', models.CharField(max_length=250)),
                ('eye_side', models.CharField(max_length=100)),
                ('answer', models.CharField(max_length=250)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='detoxa_services.users')),
            ],
            options={
                'db_table': 'eye_sight_tracker',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ChildTracker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=40)),
                ('age', models.IntegerField()),
                ('height', models.IntegerField()),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], default='Male', max_length=10)),
                ('result', models.FloatField(null=True)),
                ('weight', models.IntegerField()),
                ('created', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('parent', models.ForeignKey(db_column='parent_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fk_parent_id', to='detoxa_services.users')),
            ],
            options={
                'db_table': 'growth_tracker',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('media_url', models.TextField(null=True)),
                ('published_on', models.DateTimeField(auto_now_add=True)),
                ('author', models.CharField(max_length=50, null=True)),
                ('key', models.CharField(max_length=255, null=True)),
                ('para1', models.TextField(null=True)),
                ('para2', models.TextField(null=True)),
                ('para3', models.TextField(null=True)),
                ('para4', models.TextField(null=True)),
                ('viewed', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('blog_category', models.ForeignKey(db_column='blog_category_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fk_blog_category_id', to='detoxa_services.blogcategory')),
            ],
            options={
                'db_table': 'blog',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=3000)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('fees', models.IntegerField(default=500)),
                ('is_completed', models.BooleanField(default=False)),
                ('is_upcoming', models.BooleanField(default=True)),
                ('is_cancelled', models.BooleanField(default=False)),
                ('is_promocode_applied', models.BooleanField(default=False)),
                ('booked_at', models.DateTimeField(auto_now_add=True)),
                ('child', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='detoxa_services.userchildrelation')),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='doctor', to='detoxa_services.doctor')),
                ('promocode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='detoxa_services.promocode')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='detoxa_services.users')),
            ],
            options={
                'db_table': 'appointment',
                'managed': True,
            },
        ),
    ]
