from rest_framework import serializers
from ..models.doctors_models import Doctor, Speciality
from django.core.validators import EmailValidator

class DoctorsSerializer(serializers.ModelSerializer):
    """
    Serializer for Doctors
    """
    image = serializers.ImageField()
    class Meta:
        model = Doctor
        fields = ['id','name', 'speciality', 'degree', 'image','experience','email','phone','time_slots','fees','is_active']
        extra_kwargs = {
                        'name': {'required': True}, 'email': {'required': True, 'validators': [EmailValidator]},
                        'phone': {'required': True}, 'degree': {'required': True},'speciality':{'required':True},
                        'experience':{'required':True}, 'fees':{'required':True}, 'time_slots':{'required':True},
                        'is_active':{'required':True},'image':{'required':True}
                        }


class DoctorSpecializtionSerializer(serializers.ModelSerializer):
    """
    Serializer for Doctor Specialization
    """
    class Meta:
        model = Speciality
        fields = ['id','name']

class ImageUploadSerializer(serializers.Serializer):
    """
    Serializer for Image Upload
    """
    image = serializers.ImageField()
