from rest_framework import serializers
from detoxa_services.models.hospitals_models import HospitalUser, Hospital


class HospitalSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    address = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=255)
    email = serializers.CharField(max_length=255)
    pincode = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=255)
    state = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    total_no_of_doctors = serializers.IntegerField(default=0)
    logo = serializers.ImageField()

class HospitalListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'
        depth = 2

class UpdateHospitalSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255,required=False)
    address = serializers.CharField(max_length=255,required=False)
    phone = serializers.CharField(max_length=255,required=False)
    email = serializers.CharField(max_length=255,required=False)
    pincode = serializers.CharField(max_length=255,required=False)
    city = serializers.CharField(max_length=255,required=False)
    state = serializers.CharField(max_length=255,required=False)
    total_no_of_doctors = serializers.IntegerField(default=0,required=False)
    logo = serializers.ImageField(required=False)

class CreateHospitalUserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    profile_pic = serializers.ImageField()
    email = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    hospital_id = serializers.IntegerField()

class UpdateHospitalUserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255,required=False)
    profile_pic = serializers.ImageField(required=False)
    email = serializers.CharField(max_length=255,required=False)
    phone = serializers.CharField(max_length=255,required=False)
    password = serializers.CharField(max_length=255,required=False)
    hospital_id = serializers.IntegerField(required=False)

class GetHospitalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalUser
        fields = '__all__'
        depth = 3
        read_only = fields
    