from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.utils.translation import ugettext_lazy as _
from detoxa_services.models.users import Users
from ..models.doctors_specialization import Specialization


class Doctors(models.Model):

    # mobile_regex = RegexValidator(regex=r'^\d{11,13}$', message=_(
    #     'Phone number must be entered in the format: 919999999999 of length 11 to 14.'))

    name = models.CharField(max_length=100, null=False)
    user = models.OneToOneField(Users, on_delete=models.SET_NULL, null=True, blank=True)
    specialization = models.ForeignKey(Specialization, db_column='specialization_id', on_delete=models.CASCADE)
    degree_name = models.CharField(max_length=50, null=True)
    experience = models.CharField(max_length=100, null=True)
    doc_image_url = models.CharField(default='', max_length=500)
    doc_image = models.CharField(default='', max_length=5000)
    # profile_image_key = models.CharField(null=True, max_length=255)
    # profile_image_extension = models.CharField(null=True, max_length=20)
    # email = models.EmailField(max_length=200, unique=True, validators=[EmailValidator], null=True)
    # mobile = models.CharField(max_length=30, unique=True, validators=[mobile_regex], null=True)
    days = models.CharField(max_length=1000, null=True)
    time_slots = models.CharField(max_length=4000, null=True)
    consultation_fee = models.IntegerField()
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'doctors'
        managed = True


class BankDetails(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=100, null=True)
    account_holder_name = models.CharField(max_length=100, null=True)
    account_number = models.CharField(max_length=100, null=True)
    ifsc_code = models.CharField(max_length=100, null=True)
    branch_name = models.CharField(max_length=100, null=True)
    account_type = models.CharField(max_length=100, null=True)
    branch_address = models.CharField(max_length=100, null=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    is_doctor = models.BooleanField(default=False)
    is_therapist = models.BooleanField(default=False)

    
    class Meta:
        db_table = 'bank_details'
        managed = True