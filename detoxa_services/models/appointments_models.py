from django.db import models
from .users import Users
from .user_child_relation import UserChildRelation
from .doctors import Doctors
from .promocode_models import Promocode

class Appointment(models.Model):
    """
    Appointment model
    """

    class AppointmentStatusChoices:
        choices = (('Pending', 'Pending'), ('Completed', 'Completed'),('Rescheduled','Rescheduled'), ('Cancelled', 'Cancelled'))
    
    user = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    doctor = models.ForeignKey(Doctors, on_delete=models.SET_NULL, null=True,blank=True, related_name='doctor')
    child = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True,related_name='child')
    description = models.TextField(max_length=3000)
    date = models.DateField()
    # time = models.TimeField()
    slot = models.CharField(default='',max_length=100)
    fees = models.IntegerField(default=500)
    # is_completed = models.BooleanField(default=False)
    # is_upcoming = models.BooleanField(default=True)
    # is_cancelled = models.BooleanField(default=False)
    status = models.CharField(choices=AppointmentStatusChoices.choices, max_length=20, default='Pending')
    is_promocode_applied = models.BooleanField(default=False)
    promocode = models.ForeignKey(Promocode,on_delete=models.SET_NULL,null=True,blank=True)
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'appointment'
