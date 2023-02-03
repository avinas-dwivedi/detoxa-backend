# Generated by Django 3.2.10 on 2022-05-27 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detoxa_services', '0120_auto_20220523_2132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feature',
            name='analytical_tracker',
        ),
        migrations.RemoveField(
            model_name='feature',
            name='blogs',
        ),
        migrations.RemoveField(
            model_name='feature',
            name='child_kits',
        ),
        migrations.RemoveField(
            model_name='feature',
            name='consultation',
        ),
        migrations.RemoveField(
            model_name='feature',
            name='contact',
        ),
        migrations.RemoveField(
            model_name='feature',
            name='covid_19',
        ),
        migrations.RemoveField(
            model_name='feature',
            name='eyesight_tracker',
        ),
        migrations.RemoveField(
            model_name='feature',
            name='food_nutrition_tracker',
        ),
        migrations.RemoveField(
            model_name='feature',
            name='growth_tracker',
        ),
        migrations.RemoveField(
            model_name='feature',
            name='hair_tracker',
        ),
        migrations.RemoveField(
            model_name='feature',
            name='hand_eye_tracker',
        ),
        migrations.RemoveField(
            model_name='feature',
            name='home',
        ),
        migrations.RemoveField(
            model_name='feature',
            name='learnability_tracker',
        ),
        migrations.RemoveField(
            model_name='feature',
            name='motorskill_tracker',
        ),
        migrations.RemoveField(
            model_name='feature',
            name='skin_tracker',
        ),
        migrations.RemoveField(
            model_name='feature',
            name='subscription',
        ),
        migrations.RemoveField(
            model_name='feature',
            name='therapy',
        ),
        migrations.RemoveField(
            model_name='feature',
            name='vaccination_tracker',
        ),
        migrations.AddField(
            model_name='feature',
            name='Analytical_Tracker_Child_Details',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Analytical_Tracker_Testimonials',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Analytical_Tracker_View_Reports',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Blogs_Categories',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Blogs_Listing',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Blogs_Trending_Blogs',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Child_Tracker_Analytical',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Child_Tracker_Eyesight',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Child_Tracker_Food_and_Nutrition',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Child_Tracker_Growth',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Child_Tracker_Hair',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Child_Tracker_Hand_and_Eye_Coordination',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Child_Tracker_Learnability',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Child_Tracker_Motor_Skill',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Child_Tracker_Skin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Child_Tracker_Vaccination',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Consultation_Search_Doctors',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Consultation_Speciality',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Consultation_Symptoms',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Covid_Avoid_Covid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Covid_Doctors',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Covid_Screen_Time',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Covid_Symptoms',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Eyesight_Tracker_Child_Details',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Eyesight_Tracker_Testimonials',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Eyesight_Tracker_View_Reports',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Food_Tracker_Child_Details',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Food_Tracker_Child_Testimonials',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Food_Tracker_Recommended_Meals',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Food_Tracker_View_Reports',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Growth_Tracker_Child_Details',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Growth_Tracker_Testimonials',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Growth_Tracker_View_Reports',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Hair_Tracker_Child_Details',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Hair_Tracker_Testimonials',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Hair_Tracker_View_Reports',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Hand_and_Eye_Tracker_Child_Details',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Hand_and_Eye_Tracker_Testimonials',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Hand_and_Eye_Tracker_View_Reports',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Home_Child_Tracker',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Home_Choose_Your_Subscription',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Home_Feedback',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Home_Latest_Video',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Home_Specialities',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Home_Why_Detoxa',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Kits_Categories',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Kits_Listing',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Learnability_Tracker_Child_Details',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Learnability_Tracker_Testimonials',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Learnability_Tracker_View_Reports',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Motor_Skill_Tracker_Child_Details',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Motor_Skill_Tracker_Testimonials',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Motor_Skill_Tracker_View_Reports',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Navigation_Bar_Blogs',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Navigation_Bar_Child_Kits',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Navigation_Bar_Child_Tracker',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Navigation_Bar_Consultation',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Navigation_Bar_Contact',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Navigation_Bar_Covid_19',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Navigation_Bar_Subscription',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Navigation_Bar_Therapy',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Skin_Tracker_Child_Details',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Skin_Tracker_Testimonials',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Skin_Tracker_View_Reports',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Subscription_Choose_Your_Subscription',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Subscription_Membership',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Subscription_Offers',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Theraoy_Symptoms',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Therapy_Search_Doctors',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Therapy_Speciality',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Vaccination_Tracker_Child_Details',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Vaccination_Tracker_Testimonials',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='feature',
            name='Vaccination_Tracker_View_Reports',
            field=models.BooleanField(default=False),
        ),
    ]