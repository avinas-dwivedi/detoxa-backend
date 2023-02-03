from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator


class MobileOTP(models.Model):
    mobile_regex = RegexValidator(regex=r'^\d{11,13}$', message=_(
        'Phone number must be entered in the format: 919999999999 of length 11 to 14.'))

    mobile_no = models.CharField(max_length=80, validators=[mobile_regex])
    otp = models.IntegerField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mobile_otp'
        managed = True