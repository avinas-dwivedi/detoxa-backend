from django.db import models
from .users import Users


class VaccinationData(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    is_active = models.BooleanField(default=True)
    min_age = models.IntegerField(null=False, default=0)
    max_age = models.IntegerField(null=False, default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vaccination_data'
        managed = True


class MyVaccinationDetails(models.Model):
    class Status(models.Model):
        status_choices = (('Booked', 'Booked'),
                          ('Done', 'Done'),
                          ('OverDue', 'OverDue'),
                          ('Upcoming', 'Upcoming'),
                          ('Cancelled', 'Cancelled'))

    vaccine = models.ForeignKey(VaccinationData, db_column='vaccine_id', related_name='fk_vaccine_id',
                                on_delete=models.CASCADE)
    user = models.ForeignKey(Users, db_column='user_id', related_name='fk_vaccine_user_id', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=Status.status_choices, default='Upcoming')
    reminder_date = models.DateField(null=True)
    reminder_time = models.TimeField(null=True)
    is_reminder_added = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'my_vaccine_details'
        managed = True

class VaccinationAppointment(models.Model):
    class VaccinationAppointmentStatus(models.Model):
        status_choices = (('Booked', 'Booked'),
                          ('Done', 'Done'),
                          ('OverDue', 'OverDue'),
                          ('Upcoming', 'Upcoming'),
                          ('Cancelled', 'Cancelled'))
    vaccine = models.ForeignKey(VaccinationData,on_delete=models.CASCADE)
    user = models.ForeignKey(Users,  on_delete=models.CASCADE)
    child = models.ForeignKey(Users, db_column='child_id', related_name='fk_vaccine_child_id', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=VaccinationAppointmentStatus.status_choices,default='Upcoming')
    vaccination_date = models.DateField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vaccination_appointment'
        managed = True