from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.utils.translation import ugettext_lazy as _


class ContactUs(models.Model):

    mobile_regex = RegexValidator(regex=r'^\d{11,13}$', message=_(
        'Phone number must be entered in the format: 919999999999 of length 11 to 14.'))

    full_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=200, validators=[EmailValidator])
    mobile = models.CharField(max_length=30, validators=[mobile_regex])
    message = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'contact_us'
        managed = True