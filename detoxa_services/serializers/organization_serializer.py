import email
from django.core import validators
from rest_framework import serializers
from detoxa_services.models import Users
from detoxa_services.models.organizations_models import Organizations, OrganizationUser
from django.core.validators import EmailValidator

from detoxa_services.models.user_child_relation import UserChildRelation

ORGANIZATION_USER_TYPE_CHOICES = (('Student', 'Student'), ('Teacher', 'Teacher'), ('Non-Teaching Staff', 'Non-Teaching Staff'), ('Flat', 'Flat'), ('Employee', 'Employee'))

class CreateOrganizationSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new organization
    """
    image = serializers.ImageField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Organizations
        fields = ['id', 'type', 'name', 'address', 'city', 'state', 'country', 'zipcode', 'phone', 'email', 'image', 'total_no_of_students',
                  'total_no_of_teachers', 'total_no_of_non_teaching_staff', 'total_no_of_flats', 'total_no_of_employee', 'password']
        extra_kwargs = {
            'type': {'required': True}, 'email': {'required': True, 'validators': [EmailValidator]},
            'name': {'required': True}, 'address': {'required': True}, 'city': {'required': True},
            'state': {'required': True}, 'country': {'required': True}, 'zipcode': {'required': True},
            'image': {'required': True}, 'phone': {'required': True}, 'password': {'required': True}
        }

class OrganizationListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing organization
    """
    class Meta:
        model = Organizations
        fields = ['id', 'type', 'name', 'address', 'city', 'state', 'country', 'zipcode', 'phone', 'email', 'total_no_of_students',
                  'total_no_of_teachers', 'total_no_of_non_teaching_staff', 'total_no_of_flats', 'total_no_of_employee','image']
        extra_kwargs = {
            'type': {'required': False}, 
            'email': {'required': False},
            'name': {'required': False},
            'address': {'required': False},
            'city': {'required': False},
            'state': {'required': False},
            'country': {'required': False},
            'zipcode': {'required': False},
            'phone': {'required': False},
            'email': {'required': False},
            'image': {'required': False},
        }
class UpdateOrganizationSerializer(serializers.ModelSerializer):
    """
    Serilaizer for updating an orgnization
    """
    image = serializers.ImageField(required=False)
    class Meta:
        model = Organizations
        fields = ['id', 'type','image', 'name', 'address', 'city', 'state', 'country', 'zipcode', 'phone', 'email', 'total_no_of_students',
                'total_no_of_teachers', 'total_no_of_non_teaching_staff', 'total_no_of_flats', 'total_no_of_employee']
        extra_kwargs = {
            'type': {'required': False},
            'image': {'required': False},
            'email': {'required': False},
            'name': {'required': False},
            'address': {'required': False},
            'city': {'required': False},
            'state': {'required': False},
            'country': {'required': False},
            'zipcode': {'required': False},
            'phone': {'required': False},
            'email': {'required': False},
        }  


class OrganizationUserSerializer(serializers.Serializer):
    """
    Serializer for creating new organization user
    """
    full_name = serializers.CharField(required=True)
    date_of_birth = serializers.DateField()
    admission_number = serializers.CharField(default='',max_length=256,required=False)
    user_class = serializers.CharField(default='',max_length=256)
    user_section = serializers.CharField(default='',max_length=256)
    father_name = serializers.CharField(default='',max_length=256)
    mother_name = serializers.CharField(default='',max_length=256)
    father_email = serializers.EmailField()
    mother_email = serializers.EmailField()
    father_phone = serializers.CharField(default='',max_length=256)
    mother_phone = serializers.CharField(default='',max_length=256)
    employee_id = serializers.CharField(default='',max_length=256)
    employee_is = serializers.CharField(default='',max_length=256)
    flat_number = serializers.CharField(default='',max_length=256,required=False)
    password = serializers.CharField(required=True)
    create_id_using_father_email = serializers.BooleanField(default=False)
    create_id_using_mother_email = serializers.BooleanField(default=False)
    type = serializers.ChoiceField(required=True,choices=ORGANIZATION_USER_TYPE_CHOICES)
    profile_pic = serializers.ImageField(required=True)

class UpdateOrganizationUserSerializer(serializers.Serializer):
    """
    Serializer for creating new organization user
    """
    full_name = serializers.CharField(required=False)
    date_of_birth = serializers.DateField(required=False)
    admission_number = serializers.CharField(default='',max_length=256,required=False)
    user_class = serializers.CharField(default='',max_length=256,required=False)
    user_section = serializers.CharField(default='',max_length=256,required=False)
    father_name = serializers.CharField(default='',max_length=256,required=False)
    mother_name = serializers.CharField(default='',max_length=256,required=False)
    father_email = serializers.EmailField(required=False)
    mother_email = serializers.EmailField(required=False)
    father_phone = serializers.CharField(default='',max_length=256,required=False)
    mother_phone = serializers.CharField(default='',max_length=256,required=False)
    employee_id = serializers.CharField(default='',max_length=256,required=False)
    employee_is = serializers.CharField(default='',max_length=256,required=False)
    flat_number = serializers.CharField(default='',max_length=256,required=False)
    password = serializers.CharField(required=False)
    create_id_using_father_email = serializers.BooleanField(default=False,required=False)
    create_id_using_mother_email = serializers.BooleanField(default=False,required=False)
    type = serializers.ChoiceField(required=False,choices=ORGANIZATION_USER_TYPE_CHOICES)
    profile_pic = serializers.ImageField(required=False)
    # class Meta:
    #     model = OrganizationUser
    #     fields = ['id', 'organization', 'user', 'type', 'created']
    #     extra_kwargs = {
    #         'id': {'read_only': True},
    #         'organization': {'required': True},
    #         'user': {'required': True},
    #         'type': {'required': True},
    #     }
    #     depth = 4


class OrganizationUserListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing organization user
    """
    class Meta:
        model = OrganizationUser
        fields = '__all__'
        # depth = 5


class SchoolUserListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing school user
    """

    full_name = serializers.SerializerMethodField()
    parent_profile_pic = serializers.SerializerMethodField()
    child_profile_pic = serializers.SerializerMethodField()
    parent_name = serializers.SerializerMethodField()
    
    class Meta:
        model = OrganizationUser
        fields = ['id', 'organization', 'user', 'type', 'created', 'full_name', 'date_of_birth',
                  'admission_number', 'user_class', 'user_section', 'father_name', 'mother_name',
                  'father_email', 'mother_email', 'father_phone', 'mother_phone', 'type',
                  'parent_profile_pic', 'child_profile_pic','parent_name']

    def get_child_profile_pic(self, obj):
        try:
            child_user = UserChildRelation.objects.filter(parent_user=obj.user)
            for i in child_user:
                child_profile_pic = Users.objects.filter(id=i.child_user_id).values_list('profile_pic_url')
            return child_profile_pic
        except Exception as e:
            return None

    def get_full_name(self, obj):
        try:
            child_user = UserChildRelation.objects.filter(parent_user=obj.user)
            child_name = ''
            for i in child_user:
                child_name = Users.objects.filter(id=i.child_user_id)[0].full_name
            return child_name
        except Exception as e:
            return None


    def get_parent_profile_pic(self, obj):
        return obj.user.profile_pic_url

    def get_parent_name(self, obj):
        return obj.user.full_name


class SocietyUserListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing society user
    """
    full_name = serializers.SerializerMethodField()
    parent_profile_pic = serializers.SerializerMethodField()
    child_profile_pic = serializers.SerializerMethodField()
    parent_name = serializers.SerializerMethodField()
    
    email = serializers.CharField(source='user.email')
    class Meta:
        model = OrganizationUser
        fields = ['id', 'organization', 'user', 'type', 'created','full_name','date_of_birth','father_name','mother_name','email','flat_number','type','parent_profile_pic', 'child_profile_pic','parent_name']

    def get_child_profile_pic(self, obj):
        try:
            child_user = UserChildRelation.objects.filter(parent_user=obj.user)
            for i in child_user:
                child_profile_pic = Users.objects.filter(id=i.child_user_id).values_list('profile_pic_url')
            return child_profile_pic
        except Exception as e:
            return None

    def get_full_name(self, obj):
        try:
            child_user = UserChildRelation.objects.filter(parent_user=obj.user)
            child_name = ''
            for i in child_user:
                child_name = Users.objects.filter(id=i.child_user_id)[0].full_name
            return child_name
        except Exception as e:
            return None


    def get_parent_profile_pic(self, obj):
        return obj.user.profile_pic_url

    def get_parent_name(self, obj):
        return obj.user.full_name

class CompanyUserListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing company user
    """

    full_name = serializers.SerializerMethodField()
    parent_profile_pic = serializers.SerializerMethodField()
    child_profile_pic = serializers.SerializerMethodField()
    parent_name = serializers.SerializerMethodField()


    class Meta:
        model = OrganizationUser
        fields = ['id', 'organization', 'user', 'type', 'employee_id','employee_is','created','full_name','date_of_birth','father_name','mother_name','type','parent_profile_pic', 'child_profile_pic','parent_name']

    def get_child_profile_pic(self, obj):
        try:
            child_user = UserChildRelation.objects.filter(parent_user=obj.user)
            for i in child_user:
                child_profile_pic = Users.objects.filter(id=i.child_user_id).values_list('profile_pic_url')
            return child_profile_pic
        except Exception as e:
            return None

    def get_full_name(self, obj):
        try:
            child_user = UserChildRelation.objects.filter(parent_user=obj.user)
            child_name = ''
            for i in child_user:
                child_name = Users.objects.filter(id=i.child_user_id)[0].full_name
            return child_name
        except Exception as e:
            return None


    def get_parent_profile_pic(self, obj):
        return obj.user.profile_pic_url

    def get_parent_name(self, obj):
        return obj.user.full_name

class OrganizationDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for listing organization details
    """
    class Meta:
        model = Organizations
        fields = '__all__'
        depth = 5
        
class OrganizationUserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for listing organization user details
    """
    class Meta:
        model = OrganizationUser
        fields = '__all__'
        depth = 5