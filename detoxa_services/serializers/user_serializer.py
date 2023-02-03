from ..models.users import Users
from rest_framework import serializers
from django.core.validators import EmailValidator


class UserSignupSerializer(serializers.ModelSerializer):
    session_id = serializers.CharField(max_length=300)
    otp = serializers.CharField(max_length=300)
    class Meta:
        model = Users
        fields = ['full_name', 'email','session_id','otp', 'password', 'mobile', 'is_tnc_accepted']
        extra_kwargs = {'full_name': {'required': True}, 'email': {'required': True, 'validators': [EmailValidator]},
                        'password': {'required': True}, 'mobile': {'required': True},'session_id': {'required': True},'otp': {'required': True},
                        'is_tnc_accepted': {'required': False, 'default': False}}

class UserSignupCreateOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id','full_name', 'email', 'password', 'mobile', 'is_tnc_accepted','is_tnc_accepted', 'is_admin','is_doctor','is_school_admin','is_society_admin','is_company_admin','is_hospital_admin','profile_pic_url']
        extra_kwargs = {'id':{'required':False,'read_only':True},'full_name': {'required': True}, 'email': {'required': True, 'validators': [EmailValidator]},
                        'password': {'required': True}, 'mobile': {'required': True},
                        'is_tnc_accepted': {'required': False, 'default': False},'is_active': {'read_only': True},'is_doctor':{'read_only':True},'is_school_admin':{'read_only':True},'is_society_admin':{'read_only':True},'is_company_admin':{'read_only':True},'is_hospital_admin':{'read_only':True},
                        'full_name': {'read_only': True}, 'is_admin': {'read_only': True, 'required': False},'profile_pic_url':{'read_only':True}}

class UserUpdateSerializer(serializers.ModelSerializer):
    profile_pic = serializers.FileField(required=False)
    class Meta:
        model = Users
        fields = ['address','profile_pic']
        extra_kwargs = {'address': {'required': True},'profile_pic': {'required': False}}
        # fields = ['full_name', 'email', 'mobile', 'is_tnc_accepted']
        # extra_kwargs = {'full_name': {'required': True}, 'email': {'required': True, 'validators': [EmailValidator]}, 'mobile': {'required': True},
        #                 'is_tnc_accepted': {'required': False, 'default': False}}

class UserUpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    class Meta:
        model = Users
        fields = ['password']
        extra_kwargs = {'password': {'required': True}}

class UserForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    # class Meta:
    #     model = Users
    #     fields = ['email']
    #     extra_kwargs = {'email': {'required': True}}
class AdminSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['full_name', 'email', 'password', 'mobile']
        extra_kwargs = {'full_name': {'required': True}, 'email': {'required': True, 'validators': [EmailValidator]},
                        'password': {'required': True}, 'mobile': {'required': False},
                        'is_tnc_accepted': {'required': False, 'default': True}}


class UserGenerateSignInOTPSerializer(serializers.ModelSerializer):
    mobile_no = serializers.CharField(max_length=30)

    class Meta:
        model = Users
        fields = ['mobile_no']
        extra_kwargs = {'mobile': {'required': True, }}


class UserSignInWithOTPSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(max_length=30)
    session_id = serializers.CharField(max_length=300)
    otp = serializers.CharField(max_length=6, min_length=6)

    class Meta:
        model = Users
        fields = ['full_name', 'email', 'mobile', 'session_id', 'otp', 'is_active', 'is_tnc_accepted', 'is_admin',
                  'is_doctor', 'is_school_admin', 'is_society_admin', 'is_company_admin']
        extra_kwargs = {'mobile': {'required': True, }, 'otp': {'required': True}, 'session_id': {'required': True},
                        'is_tnc_accepted': {'read_only': True}, 'is_active': {'read_only': True},
                        'is_doctor': {'read_only': True}, 'is_school_admin': {'read_only': True},
                        'is_society_admin': {'read_only': True}, 'is_company_admin': {'read_only': True}, 'is_hospital_admin':{'read_only':True},
                        'full_name': {'read_only': True}, 'email': {'read_only': True}, 'is_admin': {'read_only': True, 'required': False}}


class UserSignInWithPasswordSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=128)
    password = serializers.CharField(max_length=18)

    class Meta:
        model = Users
        fields = ['id', 'full_name', 'email', 'password', 'mobile', 'is_active', 'is_tnc_accepted', 'is_admin',
                  'is_doctor', 'is_school_admin', 'is_society_admin', 'is_company_admin', 'is_hospital_admin',
                  'is_therapist', 'profile_pic_url']
        extra_kwargs = {'email': {'required': True, 'validators': [EmailValidator]}, 'password': {'required': True},
                        'is_tnc_accepted': {'read_only': True}, 'is_active': {'read_only': True},
                        'is_doctor': {'read_only': True}, 'is_school_admin': {'read_only': True}, 'is_society_admin': {'read_only': True},
                        'is_company_admin': {'read_only': True}, 'is_hospital_admin': {'read_only': True},
                        'full_name': {'read_only': True}, 'mobile': {'read_only': True}, 'is_admin': {'read_only': True, 'required': False},
                        'is_therapist': {'read_only': True, 'required': False}, 'profile_pic_url': {'read_only': True}}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'full_name', 'email', 'mobile', 'is_active', 'is_tnc_accepted','profile_pic_url']