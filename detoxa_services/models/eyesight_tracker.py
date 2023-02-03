from django.db import models
from .users import Users


class EyeSightTracker(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    child = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True,related_name='eye_sight_child')
    test_name_answer = models.JSONField(max_length=250)
    test_type = models.CharField(max_length=100, null=True)
    # answer = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    # eye_side = models.CharField(max_length=100)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'eye_sight_tracker'
        managed = True
