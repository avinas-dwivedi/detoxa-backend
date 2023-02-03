from django.db import models
from detoxa_services.models.therapist import Therapist
from detoxa_services.models.users import Users
from detoxa_services.models.doctors import Doctors


class Favourites(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE,null=True)
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)