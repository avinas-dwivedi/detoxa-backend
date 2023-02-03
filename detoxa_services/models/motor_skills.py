from django.db import models
from .users import Users
from ..constants import constants

AGE_GROUPS_CHOICES = (('2-3 Months', '2-3 Months'), ('3 Months to 1 Yr', '3 Months to 1 Yr'),
                      ('1 Yr to 3 Yr', '1 Yr to 3 Yr'), ('3 Yr to 10 Yr', '3 Yr to 10 Yr'))


class MotorSkillTracker(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    child_user = models.ForeignKey(Users, db_column='motor_skill_child_user_id', on_delete=models.CASCADE,
                                   related_name='fk_motor_skill_child_user', null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class MotorSkillTrackerSectionAnswers(models.Model):
    motor_skill_tracker = models.ForeignKey(MotorSkillTracker, on_delete=models.CASCADE,
                                            related_name='fk_motor_skill_tracker_id',
                                            null=True)
    age_group = models.CharField(max_length=50, choices=AGE_GROUPS_CHOICES,blank=True, null=True)
    answers = models.JSONField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

