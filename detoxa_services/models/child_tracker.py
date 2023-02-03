from django.db import models
from .users import Users


class ChildTracker(models.Model):

    class ChildGenderChoice(models.Model):
        CHILD_GENDER_CHOICES = (('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others'))

    parent = models.ForeignKey(Users, db_column='parent_id', on_delete=models.CASCADE, related_name='fk_parent_id', null=True)
    child = models.ForeignKey(Users, db_column='child_id', on_delete=models.CASCADE, related_name='fk_child_id', null=True)
    # first_name = models.CharField(max_length=40, null=False)
    # last_name = models.CharField(max_length=40, null=False)
    age = models.IntegerField(null=False)
    height = models.IntegerField(null=False)
    gender = models.CharField(max_length=10, choices=ChildGenderChoice.CHILD_GENDER_CHOICES, default='Male')
    result = models.FloatField(null=True)
    weight = models.IntegerField(null=False)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'growth_tracker'
        managed = True
