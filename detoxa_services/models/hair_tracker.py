from django.db import models
from .users import Users
from ..constants import constants


class HairTracker(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    child_user = models.ForeignKey(Users, db_column='child_user_id', on_delete=models.CASCADE,
                                   related_name='fk_hair_child_user', null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hair_tracker'
        managed = True


class HairTrackerSectionAnswers(models.Model):
    hair_tracker = models.ForeignKey(HairTracker, on_delete=models.CASCADE,
                                     related_name='fk_hair_tracker_id', null=True)
    section_name = models.CharField(max_length=50, choices=constants.HAIR_TRACKER_SECTION_CHOICE)
    answer = models.IntegerField(choices=constants.ANSWER_CHOICE, default='5')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hair_tracker_section_answers'
        managed = True
