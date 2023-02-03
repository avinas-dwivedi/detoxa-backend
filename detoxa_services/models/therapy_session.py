from django.db import models
from .users import Users
from .therapist import Therapist
from .promocode_models import Promocode


class TherapySession(models.Model):

    class TherapyStatusChoices:
        choices = (('Pending', 'Pending'), ('Completed', 'Completed'), ('Rescheduled', 'Rescheduled'), ('Cancelled', 'Cancelled'))

    user = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    therapist = models.ForeignKey(Therapist, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='therapist_id')
    child = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, related_name='child_id')
    description = models.TextField(max_length=3000)
    date = models.DateField()
    slot = models.CharField(default='', max_length=100)
    fees = models.IntegerField(default=500)
    status = models.CharField(choices=TherapyStatusChoices.choices, max_length=20, default='Pending')
    is_promo_code_applied = models.BooleanField(default=False)
    promo_code = models.ForeignKey(Promocode, on_delete=models.SET_NULL, null=True, blank=True)
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'therapy_session'
