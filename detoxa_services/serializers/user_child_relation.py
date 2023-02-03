from django.core.validators import RegexValidator, EmailValidator
from rest_framework import serializers

from detoxa_services.models.user_child_relation import UserChildRelation
from ..models.users import Users
from ..constants import constants
from rest_framework import exceptions


class AddChildUserSerializer(serializers.ModelSerializer):
    # relation = serializers.CharField(required=True, allow_null=True)
    picture_url = serializers.FileField(write_only=True, required=False, allow_null=True)

    def validate(self, data):
        media_file_obj = data.get('picture_url')
        if media_file_obj:
            media_file_size = data.get('picture_url').size

            if media_file_size > constants.MEDIA_FILE_SIZE_IMAGE:
                raise exceptions.ValidationError("The maximum file size that can be uploaded is 10 MB")
            else:
                return data
        else:
            return data

    class Meta:
        model = Users
        fields = ['full_name', 'dob', 'gender', 'age', 'picture_url']
        extra_kwargs = {
            'email': {'required': False, 'validators': [EmailValidator]},
            'picture_url': {'required': True}
        }


class UpdateChildUserSerializer(serializers.ModelSerializer):
    picture_url = serializers.FileField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Users
        fields = ['full_name', 'dob', 'gender', 'age', 'picture_url']
        extra_kwargs = {
            'email': {'required': False, 'validators': [EmailValidator]},
            'picture_url': {'required': True}
        }


class GetChildUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'dob', 'gender']


class ChildDetailsSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='child_user.full_name')
    gender = serializers.CharField(source='child_user.gender')
    mobile = serializers.CharField(source='child_user.mobile')
    profile_pic_url = serializers.CharField(source='child_user.profile_pic_url')
    age = serializers.CharField(source='child_user.age')
    dob = serializers.CharField(source='child_user.dob')
    email = serializers.CharField(source='child_user.email')
    is_active = serializers.CharField(source='child_user.is_active')

    class Meta:
        model = UserChildRelation
        fields = ['id', 'full_name', 'gender', 'mobile', 'profile_pic_url', 'age', 'dob', 'email', 'is_active']
        # fields = '__all__'
        # depth = 3


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'full_name', 'email', 'mobile', 'mobile_code', 'address', 'gender', 'profile_pic_url']
