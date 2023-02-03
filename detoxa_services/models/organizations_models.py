from django.db import models
from detoxa_services.models.users import Users


class Organizations(models.Model):

    class OrganizationType(models.Model):
        ORGANIZATION_CHOICES = (('School', 'School'), ('Society', 'Society'),('Company','Company'))

    user = models.OneToOneField(Users, on_delete=models.SET_NULL, null=True,blank=True)
    type = models.CharField(choices=OrganizationType.ORGANIZATION_CHOICES, max_length=256)
    name = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    city = models.CharField(max_length=256)
    state = models.CharField(max_length=256)
    country = models.CharField(max_length=256)
    zipcode = models.CharField(max_length=256)
    phone = models.CharField(max_length=256)
    email = models.EmailField(max_length=256)
    image = models.URLField()
    total_no_of_students = models.IntegerField(default=0)
    total_no_of_teachers = models.IntegerField(default=0)
    total_no_of_non_teaching_staff = models.IntegerField(default=0)
    total_no_of_flats = models.IntegerField(default=0)
    total_no_of_employee = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

class OrganizationUser(models.Model):
    class OrganizationUserType(models.Model):
        ORGANIZATION_USER_TYPE_CHOICES = (('Student', 'Student'), ('Teacher', 'Teacher'), ('Non-Teaching Staff', 'Non-Teaching Staff'), ('Flat', 'Flat'), ('Employee', 'Employee'))

    organization = models.ForeignKey(Organizations, on_delete=models.CASCADE, related_name='organization_id')
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='organization_user_id')
    date_of_birth = models.DateField()
    admission_number = models.CharField(default='',max_length=256,)
    user_class = models.CharField(default='',max_length=256)
    user_section = models.CharField(default='',max_length=256)
    father_name = models.CharField(default='',max_length=256)
    mother_name = models.CharField(default='',max_length=256)
    father_email = models.EmailField()
    mother_email = models.EmailField()
    father_phone = models.CharField(default='',max_length=256)
    mother_phone = models.CharField(default='',max_length=256)
    flat_number = models.CharField(default='',max_length=256)
    employee_id = models.CharField(default='',max_length=256)
    employee_is = models.CharField(default='',max_length=256)
    type = models.CharField(choices=OrganizationUserType.ORGANIZATION_USER_TYPE_CHOICES, max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
