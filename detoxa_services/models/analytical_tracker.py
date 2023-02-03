from django.db import models
from .users import Users


class AnalyticalTracker(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    child = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, related_name='analytical_tracker_child')
    test_answer = models.JSONField(max_length=250)
    test_type = models.CharField(max_length=100, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'analytical_tracker'
        managed = True
