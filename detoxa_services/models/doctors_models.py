from django.db import models

from detoxa_services.models.users import Users

class Speciality(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    user = models.OneToOneField(Users, on_delete=models.SET_NULL, null=True,blank=True)
    name = models.CharField(max_length=256)
    # speciality = models.CharField(max_length=256)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    degree = models.CharField(max_length=256)
    # image = models.ImageField(upload_to='media', null=True, blank=True)
    image = models.CharField(max_length=2560, null=True, blank=True)
    experience = models.FloatField(max_length=256)
    email = models.EmailField(max_length=50)    
    phone = models.CharField(max_length=50)
    time_slots = models.CharField(max_length=256)
    fees = models.FloatField(max_length=256)
    is_active = models.BooleanField(default=True)   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'doctor'
        managed = True


