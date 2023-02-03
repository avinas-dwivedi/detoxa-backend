from django.db import models
from .users import Users
from ..constants import constants


class SkinTracker(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    child_user = models.ForeignKey(Users, db_column='child_user_id', on_delete=models.CASCADE,
                                   related_name='skin_child_user', null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'skin_tracker'
        managed = True


class SkinTrackerSectionAnswers(models.Model):
    skin_tracker = models.ForeignKey(SkinTracker, on_delete=models.CASCADE,
                                     related_name='skin_tracker_id', null=True)
    section_name = models.CharField(max_length=50, choices=constants.SECTION_CHOICE)
    answer = models.IntegerField(choices=constants.ANSWER_CHOICE, default='5')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'skin_tracker_section_answers'
        managed = True
