import email
import os
from unicodedata import name
import boto3
from drf_yasg import openapi
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from drf_yasg.utils import swagger_auto_schema
from rest_framework.pagination import PageNumberPagination
from rest_framework.serializers import Serializer
from detoxa_services.models.doctors import Doctors
from detoxa_services.models.doctors_models import Doctor
from detoxa_services.models.hospitals_models import Hospital
from detoxa_services.models.notification_models import UserDatabaseForNotification
from detoxa_services.models.user_child_relation import UserChildRelation
from detoxa_services.utils.user_authentication import UserAuthentication
from ..models.users import Users
from ..models.organizations_models import OrganizationUser, Organizations
from ..serializers.organization_serializer import CompanyUserListSerializer, CreateOrganizationSerializer, OrganizationDetailsSerializer, OrganizationListSerializer, OrganizationUserDetailSerializer, OrganizationUserListSerializer, OrganizationUserSerializer, SchoolUserListSerializer, SocietyUserListSerializer, UpdateOrganizationSerializer, UpdateOrganizationUserSerializer
from django.db.models.functions import TruncMonth, ExtractMonth
from django.db import connection
from django.db.models import Sum, Count


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10


class CreateOrganizationView(CreateAPIView):
    """
    API to register a new organization using admin panel
    """
    model = Organizations
    serializer_class = CreateOrganizationSerializer
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        if logged_in_user.is_admin:
            serializer = CreateOrganizationSerializer(data=request.data)
            if serializer.is_valid():
                type = serializer.validated_data.get('type')
                name = serializer.validated_data.get('name')
                address = serializer.validated_data.get('address')
                city = serializer.validated_data.get('city')
                image = serializer.validated_data.get('image')
                state = serializer.validated_data.get('state')
                email = serializer.validated_data.get('email')
                phone = serializer.validated_data.get('phone')
                country = serializer.validated_data.get('country')
                zipcode = serializer.validated_data.get('zipcode')
                password = serializer.validated_data.get('password')
                total_no_of_students = serializer.validated_data.get(
                    'total_no_of_students')
                total_no_of_teachers = serializer.validated_data.get(
                    'total_no_of_teachers')
                total_no_of_non_teaching_staff = serializer.validated_data.get(
                    'total_no_of_non_teaching_staff')
                total_no_of_flats = serializer.validated_data.get(
                    'total_no_of_flats')
                total_no_of_employee = serializer.validated_data.get(
                    'total_no_of_employee')
                user = Users.objects.create(
                    full_name=name, email=email, mobile=phone)
                user.password = make_password(password)
                if type == 'School':
                    user.is_school_admin = True
                elif type == 'Society':
                    user.is_society_admin = True
                elif type == 'Company':
                    user.is_company_admin = True
                user.save()
                UserDatabaseForNotification.objects.create(name=user.full_name, phone_number=user.mobile, email=user.email)
                organization_obj = Organizations.objects.create(
                    user=user,
                    type=type,
                    name=name,
                    address=address,
                    city=city,
                    state=state,
                    country=country,
                    zipcode=zipcode,
                    phone=phone,
                    email=email,
                )
                if total_no_of_students:
                    organization_obj.total_no_of_students = total_no_of_students
                    organization_obj.save()
                if total_no_of_teachers:
                    organization_obj.total_no_of_teachers = total_no_of_teachers
                    organization_obj.save()
                if total_no_of_non_teaching_staff:
                    organization_obj.total_no_of_non_teaching_staff = total_no_of_non_teaching_staff
                    organization_obj.save()
                if total_no_of_flats:
                    organization_obj.total_no_of_flats = total_no_of_flats
                    organization_obj.save()
                if total_no_of_employee:
                    organization_obj.total_no_of_employee = total_no_of_employee
                    organization_obj.save()
                if image:
                    try:
                        s3 = boto3.resource('s3', region_name='us-east-2',
                                            aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                            aws_secret_access_key='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')
                        s3.Bucket('detoxa').put_object(Key=image.name, Body=image, ACL='public-read',
                                                       ContentType=image.content_type, ContentDisposition='inline')
                        organization_obj.image = f"https://detoxa.s3.us-east-2.amazonaws.com/{image.name}"
                        organization_obj.save()
                    except Exception as e:
                        print(e)
                organization_obj_dict = {'id': organization_obj.id}
                organization_obj_dict.update(serializer.data)
                organization_obj_dict.update({'image': organization_obj.image})
                return Response(organization_obj_dict, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'You are not authorized to perform this action', 'status': status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED)


class GetOrganizationsListView(ListAPIView):
    '''
    List all organizations by passing organization_type as query parameter
    '''
    model = Organizations
    serializer_class = OrganizationListSerializer
    pagination_class = StandardResultsSetPagination
    authentication_class = []
    org_param = openapi.Parameter('organization_type', openapi.IN_QUERY, description="Organization type should be passed to get the list of organizations based on their type. If no organzation is passed then the repsonse will be an empty queryset",
                                  required=True, type=openapi.TYPE_STRING, enum=['School', 'Society', 'Company'])
    org_state_param = openapi.Parameter(
        'state', openapi.IN_QUERY, description="Organization state should be passed to get the list of organizations based on their state.", required=False, type=openapi.TYPE_STRING)
    org_email_param = openapi.Parameter(
        'email', openapi.IN_QUERY, description="Organization filter should be passed to get the list of organizations based on their email filter value.", required=False, type=openapi.TYPE_STRING)
    org_name_param = openapi.Parameter(
        'name', openapi.IN_QUERY, description="Organization filter should be passed to get the list of organizations based on their name filter value.", required=False, type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[org_param, org_name_param, org_email_param, org_state_param])
    def get(self, request, *args, **kwargs):
        organization_type = request.query_params.get('organization_type')
        state = request.query_params.get('state')
        name = request.query_params.get('name')
        email = request.query_params.get('email')
        total_organization_count = Organizations.objects.filter(
            type=organization_type, is_active=True).count()
        if state:
            organizations_list = Organizations.objects.filter(
                type=organization_type, state=state, is_active=True).order_by('-id')
            page = self.paginate_queryset(organizations_list)
            serializer = OrganizationListSerializer(page, many=True)
            return Response({'data': serializer.data, 'count': total_organization_count},  status=status.HTTP_200_OK)
        if name:
            organizations_list = Organizations.objects.filter(
                type=organization_type, name__icontains=name, is_active=True).order_by('-id')
            page = self.paginate_queryset(organizations_list)
            serializer = OrganizationListSerializer(page, many=True)
            return Response({'data': serializer.data, 'count': total_organization_count}, status=status.HTTP_200_OK)
        if email:
            organizations_list = Organizations.objects.filter(
                type=organization_type, email__icontains=email, is_active=True).order_by('-id')
            page = self.paginate_queryset(organizations_list)
            serializer = OrganizationListSerializer(page, many=True)
            return Response({'data': serializer.data, 'count': total_organization_count}, status=status.HTTP_200_OK)
        organizations_list = Organizations.objects.filter(
            type=organization_type, is_active=True).order_by('-id')
        page = self.paginate_queryset(organizations_list)
        serializer = OrganizationListSerializer(page, many=True)
        return Response({'data': serializer.data, 'count': total_organization_count}, status=status.HTTP_200_OK)


class UpdateOrganization(UpdateAPIView):
    '''
    API to Update an organization from admin panel by passing it's id as an identifier
    '''
    model = Organizations
    serializer_class = UpdateOrganizationSerializer
    parser_classes = [MultiPartParser]

    def put(self, request, *args, **kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        if logged_in_user.is_admin:
            organization_obj = Organizations.objects.get(id=kwargs.get('pk'))
            serializer = UpdateOrganizationSerializer(
                organization_obj, data=request.data)
            if serializer.is_valid():
                if serializer.validated_data.get('type'):
                    organization_obj.type = serializer.validated_data.get(
                        'type')
                if serializer.validated_data.get('name'):
                    organization_obj.name = serializer.validated_data.get(
                        'name')
                if serializer.validated_data.get('address'):
                    organization_obj.address = serializer.validated_data.get(
                        'address')
                if serializer.validated_data.get('city'):
                    organization_obj.city = serializer.validated_data.get(
                        'city')
                if serializer.validated_data.get('state'):
                    organization_obj.state = serializer.validated_data.get(
                        'state')
                if serializer.validated_data.get('country'):
                    organization_obj.country = serializer.validated_data.get(
                        'country')
                if serializer.validated_data.get('zipcode'):
                    organization_obj.zipcode = serializer.validated_data.get(
                        'zipcode')
                if serializer.validated_data.get('phone'):
                    organization_obj.phone = serializer.validated_data.get(
                        'phone')
                if serializer.validated_data.get('email'):
                    organization_obj.email = serializer.validated_data.get(
                        'email')
                if serializer.validated_data.get('total_no_of_students'):
                    organization_obj.total_no_of_students = serializer.validated_data.get(
                        'total_no_of_students')
                if serializer.validated_data.get('total_no_of_teachers'):
                    organization_obj.total_no_of_teachers = serializer.validated_data.get(
                        'total_no_of_teachers')
                if serializer.validated_data.get('total_no_of_non_teaching_staff'):
                    organization_obj.total_no_of_non_teaching_staff = serializer.validated_data.get(
                        'total_no_of_non_teaching_staff')
                if serializer.validated_data.get('total_no_of_flats'):
                    organization_obj.total_no_of_flats = serializer.validated_data.get(
                        'total_no_of_flats')
                if serializer.validated_data.get('total_no_of_employee'):
                    organization_obj.total_no_of_employee = serializer.validated_data.get(
                        'total_no_of_employee')
                organization_obj.save()

                if serializer.validated_data.get('image'):
                    try:
                        s3 = boto3.resource('s3', region_name='us-east-2',
                                            aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                            aws_secret_access_key='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')
                        s3.Bucket('detoxa').put_object(Key=serializer.validated_data.get('image').name, Body=serializer.validated_data.get('image'), ACL='public-read',
                                                       ContentType=serializer.validated_data.get('image').content_type, ContentDisposition='inline')
                        organization_obj.image = f"https://detoxa.s3.us-east-2.amazonaws.com/{serializer.validated_data.get('image').name}"
                        organization_obj.save()
                    except Exception as e:
                        print(e)
                return Response({'message': 'Organization updated successfully', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'You are not authorized to perform this action', 'status': status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED)


class CreateOrganizationUserAPIView(CreateAPIView):
    serializer_class = OrganizationUserSerializer
    model = OrganizationUser
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        if logged_in_user.is_admin or logged_in_user.is_school_admin or logged_in_user.is_society_admin or logged_in_user.is_company_admin:
            try:
                serializer = OrganizationUserSerializer(data=request.data)
                if serializer.is_valid():
                    if not serializer.validated_data.get('create_id_using_father_email') and not serializer.validated_data.get('create_id_using_mother_email'):
                        return Response({'message': 'Please select atleast one option from mother and father email id to true to create account', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
                    # import ipdb
                    # ipdb.set_trace()
                    image_url = None
                    user_obj = None
                    if serializer.validated_data.get('profile_pic'):
                        try:
                            s3 = boto3.resource('s3', region_name='us-east-2',
                                                aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                                aws_secret_access_key='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')
                            s3.Bucket('detoxa').put_object(Key=serializer.validated_data.get('profile_pic').name,
                                                           Body=serializer.validated_data.get(
                                                               'profile_pic'),
                                                           ACL='public-read',
                                                           ContentType=serializer.validated_data.get('profile_pic').content_type, ContentDisposition='inline')

                            image_url = f"https://detoxa.s3.us-east-2.amazonaws.com/{serializer.validated_data.get('profile_pic').name}"
                        except Exception as e:
                            print(e)
                    if serializer.validated_data.get('create_id_using_father_email') and not serializer.validated_data.get('create_id_using_mother_email') and not (serializer.validated_data.get('type') == 'Flat' or serializer.validated_data.get('type') == 'Employee'):
                        child_user_obj = Users.objects.create(
                            full_name=serializer.validated_data.get('full_name'), profile_pic_url=image_url)
                        user_obj = Users.objects.create(
                            full_name=serializer.validated_data.get(
                                'father_name'),
                            email=serializer.validated_data.get(
                                'father_email'),
                            mobile=serializer.validated_data.get(
                                'father_phone'),
                        )
                        user_obj.password = make_password(
                            serializer.validated_data.get('password'))
                        user_obj.save()
                        UserDatabaseForNotification.objects.create(name=user_obj.full_name, phone_number=user_obj.mobile, email=user_obj.email)
                        UserChildRelation.objects.create(
                            parent_user=user_obj,
                            child_user=child_user_obj,
                        )
                    organization_obj = Organizations.objects.filter(
                        user=logged_in_user).first()
                    if organization_obj:
                        if serializer.validated_data.get('create_id_using_mother_email') and not serializer.validated_data.get('create_id_using_father_email') and not (serializer.validated_data.get('type') == 'Flat' or serializer.validated_data.get('type') == 'Employee'):
                            child_user_obj = Users.objects.create(
                                full_name=serializer.validated_data.get('full_name'), profile_pic_url=image_url)
                            user_obj = Users.objects.create(
                                full_name=serializer.validated_data.get(
                                    'mother_name'),
                                email=serializer.validated_data.get(
                                    'mother_email'),
                                mobile=serializer.validated_data.get(
                                    'mother_phone'),
                            )
                            user_obj.password = make_password(
                                serializer.validated_data.get('password'))
                            user_obj.save()
                            UserChildRelation.objects.create(
                                parent_user=user_obj,
                                child_user=child_user_obj,
                            )
                        if serializer.validated_data.get('type') == 'Flat' or serializer.validated_data.get('type') == 'Employee':
                            user_obj = Users.objects.create(
                            full_name=serializer.validated_data.get('full_name'), profile_pic_url=image_url)
                            user_obj.password = make_password(
                                serializer.validated_data.get('password'))
                            user_obj.save()
                        OrganizationUser.objects.create(user=user_obj, organization=organization_obj,
                                                        type=serializer.validated_data.get(
                                                            'type'),
                                                        date_of_birth=serializer.validated_data.get(
                                                            'date_of_birth'),
                                                        admission_number=serializer.validated_data.get(
                                                            'admission_number'),
                                                        user_class=serializer.validated_data.get(
                                                            'user_class'),
                                                        user_section=serializer.validated_data.get(
                                                            'user_section'),
                                                        father_name=serializer.validated_data.get(
                                                            'father_name'),
                                                        mother_name=serializer.validated_data.get(
                                                            'mother_name'),
                                                        father_email=serializer.validated_data.get(
                                                            'father_email'),
                                                        mother_email=serializer.validated_data.get(
                                                            'mother_email'),
                                                        father_phone=serializer.validated_data.get(
                                                            'father_phone'),
                                                        mother_phone=serializer.validated_data.get(
                                                            'mother_phone'),
                                                        employee_id=serializer.validated_data.get(
                                                            'employee_id'),
                                                        employee_is=serializer.validated_data.get(
                                                            'employee_is'),
                                                        flat_number=serializer.validated_data.get(
                                                            'flat_number'),
                                                        )
                        return Response({'message': 'Organization user created successfully', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
                    else:
                        return Response({'message': 'Organization does not exists for the logged in user', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'message': str(e), 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'You are not authorized to perform this action', 'status': status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED)


class GetOrganizatonUsersList(ListAPIView):
    serializer_class = OrganizationUserListSerializer
    model = OrganizationUser
    parser_classes = [MultiPartParser]
    pagination_class = StandardResultsSetPagination

    org_param = openapi.Parameter('organization_type', openapi.IN_QUERY, description="Organization type should be passed to get the list of organizations based on their type. If no organzation is passed then the repsonse will be an empty queryset",
                                  required=True, type=openapi.TYPE_STRING, enum=['School', 'Society', 'Company'])
    org_email_param = openapi.Parameter(
        'email', openapi.IN_QUERY, description="Organization filter should be passed to get the list of organizations user based on their email filter value.", required=False, type=openapi.TYPE_STRING)
    org_name_param = openapi.Parameter(
        'name', openapi.IN_QUERY, description="Organization filter should be passed to get the list of organizations user based on their name filter value.", required=False, type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[org_param, org_name_param, org_email_param])
    def get(self, request, *args, **kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        # import ipdb; ipdb.set_trace()
        if logged_in_user.is_admin or logged_in_user.is_school_admin or logged_in_user.is_society_admin or logged_in_user.is_company_admin:
            organization_obj = Organizations.objects.filter(
                user=logged_in_user).first()
            total_count = OrganizationUser.objects.filter(
                organization=organization_obj, is_active=True).count()
            name = request.query_params.get('name')
            email = request.query_params.get('email')

            if organization_obj.type == 'School':
                user_obj = OrganizationUser.objects.filter(
                    organization=organization_obj, is_active=True).order_by('-id')
                page = self.paginate_queryset(user_obj)
                serializer = SchoolUserListSerializer(page, many=True)
                return Response({'message': 'Organization users list', 'status': status.HTTP_200_OK, 'data': serializer.data, 'count': total_count}, status=status.HTTP_200_OK)

            if organization_obj.type == 'School' and name:
                user_obj = OrganizationUser.objects.filter(organization=organization_obj,
                                                           user__full_name__icontains=name, is_active=True).order_by('-id')
                page = self.paginate_queryset(user_obj)
                serializer = SchoolUserListSerializer(page, many=True)
                return Response({'message': 'Organization users list', 'status': status.HTTP_200_OK, 'data': serializer.data, 'count': total_count}, status=status.HTTP_200_OK)

            if organization_obj.type == 'School' and email:
                user_obj = OrganizationUser.objects.filter(
                    organization=organization_obj, user__email__icontains=email, is_active=True).order_by('-id')
                page = self.paginate_queryset(user_obj)
                serializer = SchoolUserListSerializer(page, many=True)
                return Response({'message': 'Organization users list', 'status': status.HTTP_200_OK, 'data': serializer.data, 'count': total_count}, status=status.HTTP_200_OK)

            if organization_obj.type == 'Society' and name:
                user_obj = OrganizationUser.objects.filter(
                    organization=organization_obj, user__full_name__icontains=name, is_active=True).order_by('-id')
                page = self.paginate_queryset(user_obj)
                serializer = SocietyUserListSerializer(page, many=True)
                return Response({'message': 'Organization users list', 'status': status.HTTP_200_OK, 'data': serializer.data, 'count': total_count}, status=status.HTTP_200_OK)

            if organization_obj.type == 'Company' and name:
                user_obj = OrganizationUser.objects.filter(
                    organization=organization_obj, user__full_name__icontains=name, is_active=True).order_by('-id')
                page = self.paginate_queryset(user_obj)
                serializer = CompanyUserListSerializer(page, many=True)
                return Response({'message': 'Organization users list', 'status': status.HTTP_200_OK, 'data': serializer.data, 'count': total_count}, status=status.HTTP_200_OK)

            if organization_obj.type == 'Society' and email:
                user_obj = OrganizationUser.objects.filter(
                    organization=organization_obj, user__email__icontains=email, is_active=True).order_by('-id')
                page = self.paginate_queryset(user_obj)
                serializer = SocietyUserListSerializer(page, many=True)
                return Response({'message': 'Organization users list', 'status': status.HTTP_200_OK, 'data': serializer.data, 'count': total_count}, status=status.HTTP_200_OK)

            if organization_obj.type == 'Company' and email:
                user_obj = OrganizationUser.objects.filter(
                    organization=organization_obj, user__email__icontains=email, is_active=True).order_by('-id')
                page = self.paginate_queryset(user_obj)
                serializer = CompanyUserListSerializer(page, many=True)
                return Response({'message': 'Organization users list', 'status': status.HTTP_200_OK, 'data': serializer.data, 'count': total_count}, status=status.HTTP_200_OK)

            if organization_obj.type == 'Society':
                user_obj = OrganizationUser.objects.filter(
                    organization=organization_obj, is_active=True).order_by('-id')
                page = self.paginate_queryset(user_obj)
                serializer = SocietyUserListSerializer(page, many=True)
                return Response({'message': 'Organization users list', 'status': status.HTTP_200_OK, 'data': serializer.data, 'count': total_count}, status=status.HTTP_200_OK)
            
            if organization_obj.type == 'Company':
                user_obj = OrganizationUser.objects.filter(
                    organization=organization_obj, is_active=True).order_by('-id')
                page = self.paginate_queryset(user_obj)
                serializer = CompanyUserListSerializer(page, many=True)
                return Response({'message': 'Organization users list', 'status': status.HTTP_200_OK, 'data': serializer.data, 'count': total_count}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'You are not authorized to perform this action', 'status': status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED)


class DeleteOrganization(GenericAPIView):
    model = Organizations

    def post(self, request, *args, **kwargs):
        organization_obj = Organizations.objects.get(id=kwargs.get('pk'))
        # organization_obj.is_active = False
        # organization_obj.save()
        organization_users_obj = OrganizationUser.objects.filter(organization=organization_obj)
        for organization_user_obj in organization_users_obj:
            # organization_user_obj.is_active = False
            # organization_user_obj.save()
            organization_user_obj.delete()
        organization_obj.delete()
        user = Users.objects.get(id=organization_obj.user.id)
        # user.is_active = False
        # user.save()
        user.delete()
        return Response({'message': 'Organization deleted successfully', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)


class DeleteOrganizationUser(GenericAPIView):
    model = OrganizationUser

    def post(self, request, *args, **kwargs):
        organization_user_obj = OrganizationUser.objects.get(
            id=kwargs.get('pk'))
        # organization_user_obj.is_active = False
        # organization_user_obj.save()
        organization_user_obj.delete()
        user = Users.objects.get(id=organization_user_obj.user.id)
        # user.is_active = False
        # user.save()
        user.delete()
        return Response({'message': 'Organization user deleted successfully', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)


class GetTotalsCount(GenericAPIView):
    year_param = openapi.Parameter(
        'year_param', openapi.IN_QUERY,  required=False, type=openapi.TYPE_STRING)
    month_param = openapi.Parameter(
        'month_param', openapi.IN_QUERY,  required=False, type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[year_param, month_param])
    def get(self, request, *args, **kwargs):
        year = request.GET.get('year_param')
        month = request.GET.get('month_param')
        if year and month:
            year = int(year)
            month = int(month)

            return Response({
                'filtered_users': Users.objects.filter(is_active=True, created__year=year, created__month=month).count(),
                'filtered_doctors': Doctors.objects.filter(is_active=True, created__year=year, created__month=month).count(),
                'filtered_schools': Organizations.objects.filter(is_active=True, type='School', created__year=year, created__month=month).count(),
                'filtered_companies': Organizations.objects.filter(is_active=True, type='Company', created__year=year, created__month=month).count(),
                'filtered_socities': Organizations.objects.filter(is_active=True, type='Society', created__year=year, created__month=month).count(),
                'filtered_hospitals': Hospital.objects.filter(is_active=True, created__year=year, created__month=month).count(),
                'users': Users.objects.filter(is_active=True).count(),
                'doctors': Doctors.objects.filter(is_active=True).count(),
                'schools': Organizations.objects.filter(is_active=True, type='School').count(),
                'companies': Organizations.objects.filter(is_active=True, type='Company').count(),
                'socities': Organizations.objects.filter(is_active=True, type='Society').count(),
                'hospitals': Hospital.objects.filter(is_active=True).count()
            },
                status=status.HTTP_200_OK)
            # return Response({
            #     'users': Users.objects.filter(is_active=True, created__month=month).count(),
            #     'doctors': Doctors.objects.filter(is_active=True, created__month=month).count(),
            #     'schools': Organizations.objects.filter(is_active=True, type='School', created__month=month).count(),
            #     'companies': Organizations.objects.filter(is_active=True, type='Company', created__month=month).count(),
            #     'socities': Organizations.objects.filter(is_active=True, type='Society', created__month=month).count(),
            #     'hospitals': Hospital.objects.filter(is_active=True, created__month=month).count()},
            #     status=status.HTTP_200_OK)
        return Response({
            'users': Users.objects.filter(is_active=True).count(),
            'doctors': Doctors.objects.filter(is_active=True).count(),
            'schools': Organizations.objects.filter(is_active=True, type='School').count(),
            'companies': Organizations.objects.filter(is_active=True, type='Company').count(),
            'socities': Organizations.objects.filter(is_active=True, type='Society').count(),
            'hospitals': Hospital.objects.filter(is_active=True).count()},
            status=status.HTTP_200_OK)


class GetOrganizationDetailsAPIView(ListAPIView):
    serializer_class = OrganizationDetailsSerializer

    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        organization_obj = Organizations.objects.get(id=id)
        serializer = OrganizationDetailsSerializer(organization_obj)
        return Response({'message': 'Organization details fetched successfully', 'status': status.HTTP_200_OK, 'data': serializer.data}, status=status.HTTP_200_OK)


class GetOrganizationUserDetailsAPIView(ListAPIView):

    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        organization_user_obj = OrganizationUser.objects.get(id=id)
        serializer = OrganizationUserDetailSerializer(organization_user_obj)
        return Response({'message': 'Organization user details fetched successfully', 'status': status.HTTP_200_OK, 'data': serializer.data}, status=status.HTTP_200_OK)


class UpdateOrganizationUserDetails(UpdateAPIView):
    serializer_class = UpdateOrganizationUserSerializer
    parser_classes = [MultiPartParser]

    def put(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        try:
            organization_user_obj = OrganizationUser.objects.get(id=id)
            serializer = UpdateOrganizationUserSerializer(
                organization_user_obj, data=request.data)
            if serializer.is_valid():
                if serializer.validated_data.get('password'):
                    organization_user_obj.user.password = make_password(
                        serializer.validated_data.get('password'))
                    organization_user_obj.save()
                if serializer.validated_data.get('type'):
                    organization_user_obj.type = serializer.validated_data.get(
                        'type')
                    organization_user_obj.save()
                if serializer.validated_data.get('date_of_birth'):
                    organization_user_obj.date_of_birth = serializer.validated_data.get(
                        'date_of_birth')
                    organization_user_obj.save()
                if serializer.validated_data.get('admission_number'):
                    organization_user_obj.admission_number = serializer.validated_data.get(
                        'admission_number')
                    organization_user_obj.save()
                if serializer.validated_data.get('user_class'):
                    organization_user_obj.user_class = serializer.validated_data.get(
                        'user_class')
                    organization_user_obj.save()
                if serializer.validated_data.get('user_section'):
                    organization_user_obj.user_section = serializer.validated_data.get(
                        'user_section')
                    organization_user_obj.save()
                if serializer.validated_data.get('father_name'):
                    organization_user_obj.father_name = serializer.validated_data.get(
                        'father_name')
                    organization_user_obj.save()
                if serializer.validated_data.get('mother_name'):
                    organization_user_obj.mother_name = serializer.validated_data.get(
                        'mother_name')
                    organization_user_obj.save()
                if serializer.validated_data.get('father_email'):
                    organization_user_obj.father_email = serializer.validated_data.get(
                        'father_email')
                    organization_user_obj.save()
                if serializer.validated_data.get('mother_email'):
                    organization_user_obj.mother_email = serializer.validated_data.get(
                        'mother_email')
                    organization_user_obj.save()
                if serializer.validated_data.get('father_phone'):
                    organization_user_obj.father_phone = serializer.validated_data.get(
                        'father_phone')
                    organization_user_obj.save()
                if serializer.validated_data.get('mother_phone'):
                    organization_user_obj.mother_phone = serializer.validated_data.get(
                        'mother_phone')
                    organization_user_obj.save()
                if serializer.validated_data.get('employee_id'):
                    organization_user_obj.employee_id = serializer.validated_data.get(
                        'employee_id')
                    organization_user_obj.save()
                if serializer.validated_data.get('employee_is'):
                    organization_user_obj.employee_type = serializer.validated_data.get(
                        'employee_is')
                    organization_user_obj.save()
                if serializer.validated_data.get('flat_number'):
                    organization_user_obj.flat_number = serializer.validated_data.get(
                        'flat_number')
                    organization_user_obj.save()
                return Response({'message': 'Organization user details updated successfully', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                return Response({'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'message': 'Organization user not found', 'status': status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)


# class GetTotalsCountPerMonth(GenericAPIView):
#     year_param = openapi.Parameter(
#         'year_param', openapi.IN_QUERY,  required=False, type=openapi.TYPE_STRING)
#     entity_param = openapi.Parameter(
#         'entity_param', openapi.IN_QUERY, required=False, type=openapi.TYPE_STRING)
#
#     @swagger_auto_schema(manual_parameters=[year_param, entity_param])
#     def get(self, request, *args, **kwargs):
#         year = request.GET.get('year_param')
#         entity_type = request.GET.get('entity_param')
#         if year and entity_type:
#             year = int(year)
#
#             # truncate_date = connection.ops.date_trunc_sql('month', 'created')
#             # qs = Users.objects.extra({'month': truncate_date}).filter(is_active=True, created__year=year)
#             # report = qs.values('month').annotate(Count('pk')).order_by('month')
#             if entity_type == '1':
#                 return Response({'filtered_users': Users.objects.filter(is_active=True, created__year=year).annotate(
#                                           month=ExtractMonth('created')).values('month').annotate(
#                                           count=Count('id')).values('month', 'count')
#                                  }, status=status.HTTP_200_OK)
#             if entity_type == '2':
#                 return Response({'filtered_doctors':
#                                      Doctors.objects.annotate(month=TruncMonth('created')).values('month').annotate(
#                                          total=Count('id'))
#                                      # Doctors.objects.filter(is_active=True, created__year=year).annotate(month=TruncMonth('created')).values('month').annotate(c=Count('id')).values('month', 'c'),
#                 }, status=status.HTTP_200_OK)
#             if entity_type == '3':
#                 return Response({'filtered_schools': Organizations.objects.filter(is_active=True, type='School', created__year=year).annotate(month=TruncMonth('created')).values('month').annotate(c=Count('id')).values('month', 'c'),
#                 }, status=status.HTTP_200_OK)
#             if entity_type == '4':
#                 return Response({'filtered_companies': Organizations.objects.filter(is_active=True, type='Company', created__year=year).annotate(month=TruncMonth('created')).values('month').annotate(c=Count('id')).values('month', 'c'),
#                 }, status=status.HTTP_200_OK)
#             if entity_type == '5':
#                 return Response({
#                     'filtered_socities': Organizations.objects.filter(is_active=True, type='Society', created__year=year).annotate(month=TruncMonth('created')).values('month').annotate(c=Count('id')).values('month', 'c'),
#                 }, status=status.HTTP_200_OK)
#             if entity_type == '6':
#                 return Response({
#                     'filtered_hospitals': Hospital.objects.filter(is_active=True, created__year=year).annotate(month=TruncMonth('created')).values('month').annotate(c=Count('id')).values('month', 'c'),
#                 }, status=status.HTTP_200_OK)




class GetTotalsCountPerMonth(GenericAPIView):
    year_param = openapi.Parameter(
        'year_param', openapi.IN_QUERY,  required=False, type=openapi.TYPE_STRING)
    entity_param = openapi.Parameter(
        'entity_param', openapi.IN_QUERY, required=False, type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[year_param, entity_param])
    def get(self, request, *args, **kwargs):
        year = request.GET.get('year_param')
        entity_type = request.GET.get('entity_param')
        if year and entity_type:
            year = int(year)

            # truncate_date = connection.ops.date_trunc_sql('month', 'created')
            # qs = Users.objects.extra({'month': truncate_date}).filter(is_active=True, created__year=year)
            # report = qs.values('month').annotate(Count('pk')).order_by('month')
            if entity_type == '1':
                return Response({
                'data': Users.objects.filter(is_active=True, created__year=year).annotate(month=TruncMonth('created')).values('month').annotate(c=Count('id')).values('month', 'c'),
                }, status=status.HTTP_200_OK)
            if entity_type == '2':
                return Response({
                'data': Doctors.objects.filter(is_active=True, created__year=year).annotate(month=TruncMonth('created')).values('month').annotate(c=Count('id')).values('month', 'c'),
                }, status=status.HTTP_200_OK)
            if entity_type == '3':
                return Response({

                'data': Organizations.objects.filter(is_active=True, type='School', created__year=year).annotate(month=TruncMonth('created')).values('month').annotate(c=Count('id')).values('month', 'c'),
                }, status=status.HTTP_200_OK)
            if entity_type == '4':
                return Response({
                'data': Organizations.objects.filter(is_active=True, type='Company', created__year=year).annotate(month=TruncMonth('created')).values('month').annotate(c=Count('id')).values('month', 'c'),
                }, status=status.HTTP_200_OK)
            if entity_type == '5':
                return Response({
                'data': Organizations.objects.filter(is_active=True, type='Society', created__year=year).annotate(month=TruncMonth('created')).values('month').annotate(c=Count('id')).values('month', 'c'),
                }, status=status.HTTP_200_OK)
            if entity_type == '6':
                return Response({
                'data': Hospital.objects.filter(is_active=True, created__year=year).annotate(month=TruncMonth('created')).values('month').annotate(c=Count('id')).values('month', 'c'),
                }, status=status.HTTP_200_OK)