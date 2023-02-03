from django.db import models
from .users import Users


class HandEyeTracker(models.Model):
    class UserGenderChoices(models.Model):
        GENDER_TYPE_CHOICES = (('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others'))

    user = models.ForeignKey(Users, db_column='user_id', on_delete=models.CASCADE, related_name='fk_user_id', null=True)
    child = models.ForeignKey(Users, db_column='child_id', on_delete=models.CASCADE, related_name='hand_eye_child_id', null=True)
    test_name = models.CharField(max_length=100)
    light_on_time = models.CharField(max_length=100)
    reaction_time = models.CharField(max_length=100)
    test_question_answer = models.JSONField()
    gender = models.CharField(max_length=20, choices=UserGenderChoices.GENDER_TYPE_CHOICES)
    average = models.FloatField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hand_eye_tracker'
        managed = True