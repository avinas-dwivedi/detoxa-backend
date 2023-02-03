from rest_framework import serializers
from ..models.therapist import Therapist, TherapistCategory
from django.core.validators import EmailValidator


class TherapistSerializer(serializers.ModelSerializer):

    therapist_time_slots = serializers.ListField(child=serializers.CharField(max_length=1000, allow_null=True))
    therapist_category = serializers.IntegerField()
    password = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=200)
    mobile = serializers.CharField(max_length=30)
    therapist_image = serializers.ImageField(required=True)

    class Meta:

        model = Therapist
        fields = ['name', 'therapist_category', 'degree_name', 'experience', 'password',
                  'therapist_time_slots', 'therapist_fee', 'is_active', 'email', 'mobile',
                  'therapist_image', 'therapist_image_url']

        extra_kwargs = {
            'name': {'required': True}, 'therapist_category': {'required': True},
            'degree_name': {'required': True}, 'password': {'required': True},
            'experience': {'required': True}, 'email': {'required': True, 'validators': [EmailValidator]},
            'mobile': {'required': True}, 'therapist_time_slots': {'required': True},
            'therapist_fee': {'required': True}, 'is_active': {'required': False}
        }


class GetTherapistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Therapist
        fields = '__all__'
        depth = 2


class TherapistCategorySerializer(serializers.ModelSerializer):
    therapist_image = serializers.ImageField(required=False)

    class Meta:
        model = TherapistCategory
        fields = ["id", "name", "therapist_image", "is_active"]


class GetTherapistCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TherapistCategory
        fields = ["id", "name", "is_active","therapist_image"]


class UpdateTherapistSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=100, required=False)
    email = serializers.CharField(max_length=100, required=False)
    phone = serializers.CharField(max_length=100, required=False)
    password = serializers.CharField(max_length=100, required=False)
    profile_pic = serializers.ImageField(required=False)
    therapist_category = serializers.IntegerField(required=False)
    degree_name = serializers.CharField(max_length=100, required=False)
    therapist_fee = serializers.CharField(max_length=100, required=False)
    experience = serializers.CharField(max_length=100, required=False)
    therapist_time_slots = serializers.CharField(max_length=100, required=False)
