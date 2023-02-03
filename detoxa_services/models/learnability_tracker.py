from django.db import models
from .users import Users
from ..constants import constants


class LearnabilityTracker(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    child_user = models.ForeignKey(Users, db_column='child_user_id', on_delete=models.CASCADE,
                                   related_name='fk_learnablity_child_user', null=True)
    # section_name = models.CharField(max_length=50, choices=constants.SECTION_CHOICE)
    # answer = models.IntegerField(choices=constants.ANSWER_CHOICE, default='5')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'learnability_tracker'
        managed = True


class LearnalityTrackerSectionAnswers(models.Model):
    learnablity_tracker = models.ForeignKey(LearnabilityTracker, on_delete=models.CASCADE,
                                            related_name='fk_learnablity_tracker_id',
                                            null=True)
    section_name = models.CharField(max_length=50, choices=constants.SECTION_CHOICE)
    answer = models.IntegerField(choices=constants.ANSWER_CHOICE, default='5')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'learnability_tracker_section_answers'
        managed = True
