from django.db import models
from detoxa_services.models.child_tracker import ChildTracker

from detoxa_services.models.learnability_tracker import LearnabilityTracker
from detoxa_services.models.eyesight_tracker import EyeSightTracker
from detoxa_services.models.hand_eye_tracker import HandEyeTracker
from detoxa_services.models.motor_skills import MotorSkillTracker
from detoxa_services.models.analytical_tracker import AnalyticalTracker
from detoxa_services.models.organizations_models import Organizations
from detoxa_services.models.skin_tracker import SkinTracker
from detoxa_services.models.hair_tracker import HairTracker
from .users import Users


class UserLearnabilityReport(models.Model):
    report_type = models.ForeignKey(LearnabilityTracker, on_delete=models.CASCADE,null=True,blank=True)
    report_name = models.CharField(default='',max_length=150)
    report_image_url = models.CharField(default='',max_length=500)
    parent_user = models.ForeignKey(Users,on_delete=models.CASCADE,related_name='parent_user')
    child_user = models.ForeignKey(Users,on_delete=models.CASCADE)
    description = models.TextField()
    height = models.CharField(default='',max_length=100,blank=True)
    age = models.CharField(default='',max_length=100,blank=True)
    weight = models.CharField(default='',max_length=100,blank=True)
    gender = models.CharField(default='',max_length=256)
    bmi = models.CharField(max_length=10,null=True,blank=True)
    report_date = models.DateTimeField(auto_now_add=True)
    report = models.CharField(default='',max_length=5000)
    is_downloaded = models.BooleanField(default=False)


class UserMotorSkillsReport(models.Model):
    report_type = models.ForeignKey(MotorSkillTracker, on_delete=models.CASCADE,null=True,blank=True)
    report_name = models.CharField(default='',max_length=150)
    report_image_url = models.CharField(default='',max_length=500)
    parent_user = models.ForeignKey(Users,on_delete=models.CASCADE,related_name='motor_skill_parent_user')
    child_user = models.ForeignKey(Users,on_delete=models.CASCADE)
    description = models.TextField()
    height = models.CharField(default='',max_length=100,blank=True)
    age = models.CharField(default='',max_length=100,blank=True)
    weight = models.CharField(default='',max_length=100,blank=True)
    gender = models.CharField(default='',max_length=256)
    bmi = models.CharField(max_length=10,null=True,blank=True)
    report_date = models.DateTimeField(auto_now_add=True)
    report = models.CharField(default='',max_length=5000)
    is_downloaded = models.BooleanField(default=False)


class UserGrowthReport(models.Model):
    report_type = models.ForeignKey(ChildTracker, on_delete=models.CASCADE,null=True,blank=True)
    report_name = models.CharField(default='', max_length=150)
    report_image_url = models.CharField(default='', max_length=500)
    parent_user = models.ForeignKey(Users, on_delete=models.CASCADE,related_name='grwoth_report_parent_user')
    child_user = models.ForeignKey(Users, on_delete=models.CASCADE)
    description = models.TextField()
    height = models.CharField(default='', max_length=100,blank=True)
    age = models.CharField(default='', max_length=100,blank=True)
    weight = models.CharField(default='', max_length=100,blank=True)
    gender = models.CharField(default='', max_length=256)
    bmi = models.CharField(max_length=10, null=True,blank=True)
    report_date = models.DateTimeField(auto_now_add=True)
    report = models.CharField(default='', max_length=5000)
    is_downloaded = models.BooleanField(default=False)


class UserEyeSightReport(models.Model):
    report_id = models.ForeignKey(EyeSightTracker, on_delete=models.CASCADE, null=True, blank=True)
    report_name = models.CharField(default='', max_length=150)
    report_image_url = models.CharField(default='', max_length=500)
    parent_user = models.ForeignKey(Users, on_delete=models.CASCADE,related_name='eyesight_report_parent_user')
    child_user = models.ForeignKey(Users, on_delete=models.CASCADE)
    description = models.TextField()
    height = models.CharField(default='', max_length=100,blank=True)
    age = models.CharField(default='', max_length=100,blank=True)
    weight = models.CharField(default='', max_length=100,blank=True)
    gender = models.CharField(default='', max_length=256)
    bmi = models.CharField(max_length=10, null=True, blank=True)
    report_date = models.DateTimeField(auto_now_add=True)
    report = models.CharField(default='', max_length=5000)
    is_downloaded = models.BooleanField(default=False)


class UserHandEyeCoordinationReport(models.Model):
    report_type = models.ForeignKey(HandEyeTracker, on_delete=models.CASCADE,null=True,blank=True)
    report_name = models.CharField(default='',max_length=150)
    report_image_url = models.CharField(default='',max_length=500)
    parent_user = models.ForeignKey(Users,on_delete=models.CASCADE,related_name='handeye_report_parent_user')
    child_user = models.ForeignKey(Users,on_delete=models.CASCADE)
    description = models.TextField()
    height = models.CharField(default='',max_length=100,blank=True)
    age = models.CharField(default='',max_length=100,blank=True)
    weight = models.CharField(default='',max_length=100,blank=True)
    gender = models.CharField(default='',max_length=256)
    bmi = models.CharField(max_length=10,null=True,blank=True)
    report_date = models.DateTimeField(auto_now_add=True)
    report = models.CharField(default='',max_length=5000)
    is_downloaded = models.BooleanField(default=False)


class UserAnalyticalReport(models.Model):
    report_id = models.ForeignKey(AnalyticalTracker, on_delete=models.CASCADE, null=True, blank=True)
    report_name = models.CharField(default='', max_length=150)
    report_image_url = models.CharField(default='',  max_length=500)
    parent_user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='analytical_report_parent_user')
    child_user = models.ForeignKey(Users, on_delete=models.CASCADE)
    description = models.TextField()
    height = models.CharField(default='', max_length=100, blank=True)
    age = models.CharField(default='', max_length=100, blank=True)
    weight = models.CharField(default='', max_length=100, blank=True)
    gender = models.CharField(default='', max_length=256)
    bmi = models.CharField(max_length=10, null=True, blank=True)
    report_date = models.DateTimeField(auto_now_add=True)
    report = models.CharField(default='', max_length=5000)
    is_downloaded = models.BooleanField(default=False)


class UserSkinReport(models.Model):
    report_type = models.ForeignKey(SkinTracker, on_delete=models.CASCADE, null=True, blank=True)
    report_name = models.CharField(default='', max_length=150)
    report_image_url = models.CharField(default='', max_length=500)
    parent_user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='skin_report_parent_user')
    child_user = models.ForeignKey(Users, on_delete=models.CASCADE)
    description = models.TextField()
    height = models.CharField(default='', max_length=100, blank=True)
    age = models.CharField(default='', max_length=100, blank=True)
    weight = models.CharField(default='', max_length=100, blank=True)
    gender = models.CharField(default='', max_length=256)
    bmi = models.CharField(max_length=10, null=True, blank=True)
    report_date = models.DateTimeField(auto_now_add=True)
    report = models.CharField(default='', max_length=5000)
    is_downloaded = models.BooleanField(default=False)


class UserHairReport(models.Model):
    report_type = models.ForeignKey(HairTracker, on_delete=models.CASCADE, null=True, blank=True)
    report_name = models.CharField(default='', max_length=150)
    report_image_url = models.CharField(default='', max_length=500)
    parent_user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='hair_report_parent_user')
    child_user = models.ForeignKey(Users, on_delete=models.CASCADE)
    description = models.TextField()
    height = models.CharField(default='', max_length=100,blank=True)
    age = models.CharField(default='', max_length=100,blank=True)
    weight = models.CharField(default='', max_length=100,blank=True)
    gender = models.CharField(default='', max_length=256)
    bmi = models.CharField(max_length=10, null=True, blank=True)
    report_date = models.DateTimeField(auto_now_add=True)
    report = models.CharField(default='', max_length=5000)
    is_downloaded = models.BooleanField(default=False)


class UserMedicalReport(models.Model):
    organization = models.ForeignKey(Organizations, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    user_class = models.CharField(default='', max_length=100)
    user_section = models.CharField(default='', max_length=100)
    year = models.CharField(default='', max_length=100)
    report_url = models.CharField(default='', max_length=500)
    report_date = models.DateTimeField(auto_now_add=True)
