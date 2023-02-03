from django.core.validators import MinLengthValidator, RegexValidator, EmailValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Users(models.Model):
    class Gender(models.Model):
        GENDER_CHOICES = (('Male', 'Male'), ('Female', 'Female'))

    mobile_regex = RegexValidator(regex=r'^\d{11,13}$', message=_(
        'Phone number must be entered in the format: 919999999999 of length 11 to 14.'))

    full_name = models.CharField(max_length=150)
    password = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, unique=True, validators=[EmailValidator], null=True)
    mobile = models.CharField(max_length=30, unique=True, validators=[mobile_regex], null=True)
    mobile_code = models.CharField(max_length=6, validators=[MinLengthValidator(6)], null=True)
    gender = models.CharField(max_length=6, choices=Gender.GENDER_CHOICES, null=True)
    profile_pic_url = models.TextField(null=True)
    key = models.CharField(max_length=255, null=True)
    dob = models.DateField(null=True)
    age = models.CharField(max_length=20, null=True)
    address = models.CharField(default='', max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_therapist = models.BooleanField(default=False)
    is_school_admin = models.BooleanField(default=False)
    is_society_admin = models.BooleanField(default=False)
    is_company_admin = models.BooleanField(default=False)
    is_hospital_admin = models.BooleanField(default=False)
    is_tnc_accepted = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'
        managed = True

    # def __str__(self):
    #     return self.email


class UserActiveTokens(models.Model):

    user = models.ForeignKey(Users, db_column='user_token_id', on_delete=models.CASCADE)
    user_token = models.CharField(max_length=1024)
    is_active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_active_tokens'
        managed = True


class Address(models.Model):
    user = models.ForeignKey(Users, related_name='users_address_id', on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    pincode = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
