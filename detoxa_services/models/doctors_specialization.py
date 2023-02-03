from django.db import models


class Specialization(models.Model):
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    specialist_image = models.CharField(default='', max_length=2000)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'specialization'
        managed = True
