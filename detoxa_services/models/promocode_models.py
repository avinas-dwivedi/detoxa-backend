from django.db import models


class Promocode(models.Model):
    code = models.CharField(max_length=100, unique=True)
    discount = models.IntegerField()
    description = models.TextField(default='')
    is_expired = models.BooleanField(default=False)

    class Meta:
        db_table = 'promocode'
        managed = True