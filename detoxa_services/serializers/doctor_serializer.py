from dataclasses import fields
from rest_framework import serializers

from detoxa_services.models.appointments_models import Appointment
from detoxa_services.models.therapy_session import TherapySession
from ..models.doctors import Doctors
from django.core.validators import EmailValidator
from ..constants import constants
from rest_framework import exceptions
from ..models.doctors_specialization import Specialization

ACCOUNT_TYPE = (('Savings','Savings'),('Current','Current'))
class DoctorSerializer(serializers.ModelSerializer):

    time_slots = serializers.ListField(child=serializers.CharField(max_length=1000, allow_null=True))
    specialization = serializers.IntegerField()
    password = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=200)
    mobile = serializers.CharField(max_length=30)
    doc_image = serializers.ImageField(required=True)

    class Meta:

        model = Doctors
        fields = ['name', 'specialization', 'degree_name', 'experience', 'password',
                  'time_slots', 'consultation_fee', 'is_active', 'email', 'mobile', 'doc_image_url', 'doc_image']

        extra_kwargs = {
            'name': {'required': True}, 'specialization': {'required': True},
            'degree_name': {'required': True}, 'password': {'required': True},
            'experience': {'required': True}, 'email': {'required': True, 'validators': [EmailValidator]},
            'mobile': {'required': True}, 'time_slots': {'required': True},
            'consultation_fee': {'required': True}, 'is_active': {'required': False}
        }


class GetAllDoctorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctors
        fields = '__all__'
        depth = 2
        # fields = ['id', 'name', 'specialization', 'degree_name', 'experience',
        #           'time_slots', 'consultation_fee', 'is_active', 'doc_image']


class SpecializationSerializer(serializers.ModelSerializer):
    specialist_image = serializers.ImageField(required=True)
    class Meta:
        model = Specialization
        fields = ["name","specialist_image", "is_active"]


class GetAllSpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ["id", "name", "specialist_image", "is_active"]


class UpdateDoctorsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=False)
    email = serializers.CharField(max_length=100, required=False)
    phone = serializers.CharField(max_length=100, required=False)
    password = serializers.CharField(max_length=100, required=False)
    profile_pic = serializers.ImageField(required=False)
    specialization = serializers.IntegerField(required=False)
    degree_name = serializers.CharField(max_length=100, required=False)
    consultation_fee = serializers.CharField(max_length=100, required=False)
    experience = serializers.CharField(max_length=100, required=False)
    # time_slots = serializers.CharField(max_length=100, required=False)
    time_slots = serializers.ListField(child=serializers.CharField(max_length=1000, allow_null=True, required=False))
    is_active = serializers.BooleanField()


class SaveBankDetailsSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    account_holder_name = serializers.CharField(max_length=100, required=True)
    account_number = serializers.CharField(max_length=100, required=True)
    ifsc_code = serializers.CharField(max_length=100, required=True)
    bank_name = serializers.CharField(max_length=100, required=True)
    branch_name = serializers.CharField(max_length=100, required=True)
    account_type = serializers.ChoiceField(choices=ACCOUNT_TYPE, required=True)
    branch_address = serializers.CharField(max_length=100, required=True)


class AppointmentSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        depth = 2

class TherapistAppointmentSerailizer(serializers.ModelSerializer):
    class Meta:
        model = TherapySession
        fields = '__all__'
        depth = 2
