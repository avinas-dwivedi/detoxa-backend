from django.db import models
from detoxa_services.models.users import Users


class TherapistCategory(models.Model):
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    therapist_image = models.CharField(default='', max_length=2000)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'therapist_category'
        managed = True


class Therapist(models.Model):
    name = models.CharField(max_length=100, null=False)
    user = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    therapist_category = models.ForeignKey(TherapistCategory, db_column='therapist_category_id', on_delete=models.CASCADE)
    degree_name = models.CharField(max_length=50, null=True)
    experience = models.CharField(max_length=100, null=True)

    therapist_image_url = models.CharField(default='', max_length=500)
    therapist_image = models.CharField(default='', max_length=5000)
    days = models.CharField(max_length=1000, null=True)
    therapist_time_slots = models.CharField(max_length=4000, null=True)
    therapist_fee = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'therapist'
        managed = True
