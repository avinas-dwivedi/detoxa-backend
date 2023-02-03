import boto3
from detoxa_services.models.notification_models import UserDatabaseForNotification
from detoxa_services.models.users import Users
from detoxa_services.models.hospitals_models import Hospital, HospitalUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView,ListAPIView,UpdateAPIView,GenericAPIView,RetrieveAPIView
from detoxa_services.serializers.hospital_serializer import CreateHospitalUserSerializer, GetHospitalUserSerializer, HospitalListSerializer, HospitalSerializer, UpdateHospitalSerializer, UpdateHospitalUserSerializer
from detoxa_services.utils.user_authentication import UserAuthentication
from django.contrib.auth.hashers import make_password
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from detoxa_services.views.organizations_views import StandardResultsSetPagination


class CreateHospitalView(CreateAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    parser_classes = [MultiPartParser]

    def post(self, request,*args,**kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        if logged_in_user.is_admin:
            serializer = HospitalSerializer(data=request.data)
            if serializer.is_valid():
                user = Users.objects.create(
                    full_name=serializer.validated_data.get('name'), email=serializer.validated_data.get('email'), mobile=serializer.validated_data.get('phone'), is_hospital_admin=True)
                user.password = make_password(serializer.validated_data.get('password'))
                user.save()
                UserDatabaseForNotification.objects.create(name=user.full_name, phone_number=user.mobile, email=user.email)
                hospital_obj = Hospital.objects.create(
                    user=user,
                    name=serializer.validated_data.get('name'),
                    address=serializer.validated_data.get('address'),
                    phone=serializer.validated_data.get('phone'),
                    email=serializer.validated_data.get('email'),
                    pincode=serializer.validated_data.get('pincode'),
                    city=serializer.validated_data.get('city'),
                    state=serializer.validated_data.get('state'),
                    total_no_of_doctors=serializer.validated_data.get('total_no_of_doctors')
                )
                if serializer.validated_data.get('logo'):
                    try:
                        s3 = boto3.resource('s3', region_name='us-east-2',
                                            aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                            aws_secret_access_key='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')
                        s3.Bucket('detoxa').put_object(Key=serializer.validated_data.get('logo').name, Body=serializer.validated_data.get('logo'), ACL='public-read',
                                                       ContentType=serializer.validated_data.get('logo').content_type, ContentDisposition='inline')
                        hospital_obj.logo = f"https://detoxa.s3.us-east-2.amazonaws.com/{serializer.validated_data.get('logo').name}"
                        hospital_obj.save()
                    except Exception as e:
                        print(e)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"message":"Hospital created successfully"},status=status.HTTP_200_OK)
        return Response({"message":"You are not authorized to create hospital"},status=status.HTTP_401_UNAUTHORIZED)

class GetHospitalListView(ListAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalListSerializer
    pagination_class = StandardResultsSetPagination

    org_state_param = openapi.Parameter('state', openapi.IN_QUERY, description="Organization state should be passed to get the list of organizations based on their state.", required=False, type=openapi.TYPE_STRING)
    org_name_param = openapi.Parameter('name', openapi.IN_QUERY, description="Organization filter should be passed to get the list of organizations based on their name filter value.", required=False, type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[org_name_param,org_state_param])
    def get(self, request, *args, **kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        total_hospitals = Hospital.objects.filter(is_active=True).count()
        if logged_in_user.is_admin:
            if request.GET.get('name'):
                hospital_list = Hospital.objects.filter(name__icontains=request.GET.get('name'),is_active=True).order_by('-id')
                page = self.paginate_queryset(hospital_list)
                serializer = HospitalListSerializer(page, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            if request.GET.get('state'):
                hospital_list = Hospital.objects.filter(state__icontains=request.GET.get('state'),is_active=True).order_by('-id')
                page = self.paginate_queryset(hospital_list)
                serializer = HospitalListSerializer(page, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            hospital_list = Hospital.objects.filter(is_active=True).order_by('-id')
            page = self.paginate_queryset(hospital_list)
            serializer = HospitalListSerializer(page, many=True)
            return Response({'data':serializer.data,'count':total_hospitals}, status=status.HTTP_200_OK)
        return Response({"message":"You are not authorized to view hospital list"},status=status.HTTP_401_UNAUTHORIZED)


class UpdateHospital(UpdateAPIView):
    serializer_class = UpdateHospitalSerializer
    parser_classes = [MultiPartParser]

    def put(self,request,*args,**kwargs):
        id = kwargs.get('pk')
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        if logged_in_user.is_admin:
            try:
                hospital_obj = Hospital.objects.get(id=id)
                serializer = UpdateHospitalSerializer(hospital_obj,data=request.data)
                if serializer.is_valid():
                    hospital_obj.name = serializer.validated_data.get('name')
                    hospital_obj.address = serializer.validated_data.get('address')
                    hospital_obj.phone = serializer.validated_data.get('phone')
                    hospital_obj.email = serializer.validated_data.get('email')
                    hospital_obj.pincode = serializer.validated_data.get('pincode')
                    hospital_obj.city = serializer.validated_data.get('city')
                    hospital_obj.state = serializer.validated_data.get('state')
                    hospital_obj.total_no_of_doctors = serializer.validated_data.get('total_no_of_doctors')
                    hospital_obj.save()
                    if serializer.validated_data.get('logo'):
                        try:
                            s3 = boto3.resource('s3', region_name='us-east-2',
                                                aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                                aws_secret_access_key='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')
                            s3.Bucket('detoxa').put_object(Key=serializer.validated_data.get('logo').name, Body=serializer.validated_data.get('logo'), ACL='public-read',
                                                        ContentType=serializer.validated_data.get('logo').content_type, ContentDisposition='inline')
                            hospital_obj.logo = f"https://detoxa.s3.us-east-2.amazonaws.com/{serializer.validated_data.get('logo').name}"
                            hospital_obj.save()
                        except Exception as e:
                            print(e)
                    return Response({"message":"Hospital updated successfully"},status=status.HTTP_200_OK)
                return Response({"message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"message":"Hospital not found"},status=status.HTTP_404_NOT_FOUND)
        return Response({"message":"You are not authorized to update hospital"},status=status.HTTP_401_UNAUTHORIZED)


class CreateHospitalUser(CreateAPIView):
    serializer_class = CreateHospitalUserSerializer
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        if logged_in_user.is_hospital_admin:
            serializer = CreateHospitalUserSerializer(data=request.data)
            if serializer.is_valid():
                profile_pic = serializer.validated_data.get('profile_pic')
                profile_pic_url = ''
                if profile_pic:
                    try:
                        s3 = boto3.resource('s3', region_name='us-east-2',
                                            aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                            aws_secret_access_key='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')
                        s3.Bucket('detoxa').put_object(Key=profile_pic.name, Body=profile_pic, ACL='public-read',
                                                    ContentType=profile_pic.content_type, ContentDisposition='inline')
                        profile_pic_url = f"https://detoxa.s3.us-east-2.amazonaws.com/{profile_pic.name}"
                    except Exception as e:
                        print(e) 
                user = Users.objects.create(
                    full_name=serializer.validated_data.get('name'),profile_pic_url=profile_pic_url, email=serializer.validated_data.get('email'), mobile=serializer.validated_data.get('phone'),is_doctor=True, is_hospital_admin=False)
                user.password = make_password(serializer.validated_data.get('password'))
                user.save()
                UserDatabaseForNotification.objects.create(name=user.full_name, phone_number=user.mobile, email=user.email)
                hospital_obj = Hospital.objects.get(id=serializer.validated_data.get('hospital_id'))
                hospital_obj.total_no_of_doctors += 1
                hospital_obj.save()
                HospitalUser.objects.create(user=user, hospital=hospital_obj)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"You are not authorized to create hospital user"},status=status.HTTP_401_UNAUTHORIZED)


class GetHospitalUsers(ListAPIView):
    serializer_class = GetHospitalUserSerializer
    pagination_class = StandardResultsSetPagination

    org_email_param = openapi.Parameter('email', openapi.IN_QUERY, description="Organization user email should be passed to get the list of organizations based on their state.", required=False, type=openapi.TYPE_STRING)
    org_name_param = openapi.Parameter('name', openapi.IN_QUERY, description="Organization user name should be passed to get the list of organizations based on their name filter value.", required=False, type=openapi.TYPE_STRING)
    
    @swagger_auto_schema(manual_parameters=[org_name_param, org_email_param])
    def get(self, request, *args, **kwargs):

        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        if logged_in_user.is_hospital_admin:
            try:
                hospital_obj = Hospital.objects.get(user=logged_in_user, is_active=True)
                total_count = HospitalUser.objects.filter(hospital=hospital_obj, is_active=True).count()
                if request.GET.get('name'):
                    hospital_obj = Hospital.objects.get(user=logged_in_user, is_active=True)
                    hospital_user_list = HospitalUser.objects.filter(hospital=hospital_obj, user__full_name__icontains=request.GET.get('name'), is_active=True)
                    page = self.paginate_queryset(hospital_user_list)
                    serializer = GetHospitalUserSerializer(page, many=True)
                    return Response({'data': serializer.data, 'count': total_count}, status=status.HTTP_200_OK)
                if request.GET.get('email'):
                    hospital_obj = Hospital.objects.get(user=logged_in_user, is_active=True)
                    hospital_user_list = HospitalUser.objects.filter(hospital=hospital_obj, user__email__icontains=request.GET.get('email'), is_active=True)
                    page = self.paginate_queryset(hospital_user_list)
                    serializer = GetHospitalUserSerializer(page, many=True)
                    return Response({'data': serializer.data, 'count': total_count}, status=status.HTTP_200_OK)
                hospital_obj = Hospital.objects.get(user=logged_in_user, is_active=True)
                hospital_user_list = HospitalUser.objects.filter(hospital=hospital_obj, is_active=True).order_by('-id')
                page = self.paginate_queryset(hospital_user_list)
                serializer = GetHospitalUserSerializer(page, many=True)
                return Response({'data': serializer.data, 'count': total_count}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": "Hospital not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "You are not authorized to view hospital user list"}, status=status.HTTP_401_UNAUTHORIZED)


class DeleteHospital(GenericAPIView):
    model = Hospital

    def post(self, request, *args, **kwargs):
        hospital_obj = Hospital.objects.get(id=kwargs.get('pk'))
        # hospital_obj.is_active = False
        # hospital_obj.save()
        hospital_users_obj = HospitalUser.objects.filter(hospital=hospital_obj)
        for hospital_user_obj in hospital_users_obj:
            # hospital_user_obj.is_active = False
            # hospital_user_obj.save()
            hospital_user_obj.delete()
        hospital_obj.delete()
        user = Users.objects.get(id=hospital_obj.user.id)
        # user.is_active = False
        # user.save()
        user.delete()
        return Response({'message': 'Hospital deleted successfully', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)


class DeleteHospitalUser(GenericAPIView):
    model = HospitalUser

    def post(self, request, *args, **kwargs):
        hospital_user_obj = HospitalUser.objects.get(user__id=kwargs.get('pk'))
        # hospital_user_obj.is_active = False
        # hospital_user_obj.save()
        hospital_user_obj.delete()
        user = Users.objects.get(id=hospital_user_obj.user.id)
        # user.is_active = False
        # user.save()
        user.delete()
        return Response({'message': 'Hospital user deleted successfully', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)

class GetHospitalDetail(RetrieveAPIView):
    serializer_class = HospitalListSerializer

    def get(self, request, *args, **kwargs):
        hospital_obj = Hospital.objects.get(id=kwargs.get('pk'))
        serializer = HospitalListSerializer(hospital_obj,many=False)
        return Response({"data":serializer.data}, status=status.HTTP_200_OK)

class GetHospitalUserDetail(RetrieveAPIView):
    serializer_class = GetHospitalUserSerializer

    def get(self, request, *args, **kwargs):
        hospital_user_obj = HospitalUser.objects.get(id=kwargs.get('pk'))
        serializer = GetHospitalUserSerializer(hospital_user_obj,many=False)
        return Response({"data":serializer.data}, status=status.HTTP_200_OK)

class UpdateHospitalUser(GenericAPIView):
    serializer_class = UpdateHospitalUserSerializer
    parser_classes = (MultiPartParser, FormParser)
    queryset = HospitalUser.objects.all()

    def put(self, request, *args, **kwargs):
        hospital_user_obj = HospitalUser.objects.get(id=kwargs.get('pk'))
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        if logged_in_user.is_hospital_admin:
            serializer = UpdateHospitalUserSerializer(data=request.data)
            if serializer.is_valid():
                profile_pic = serializer.validated_data.get('profile_pic')
                profile_pic_url = ''
                if profile_pic:
                    try:
                        s3 = boto3.resource('s3', region_name='us-east-2',
                                            aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                            aws_secret_access_key='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')
                        s3.Bucket('detoxa').put_object(Key=profile_pic.name, Body=profile_pic, ACL='public-read',
                                                    ContentType=profile_pic.content_type, ContentDisposition='inline')
                        profile_pic_url = f"https://detoxa.s3.us-east-2.amazonaws.com/{profile_pic.name}"
                    except Exception as e:
                        print(e) 
                hospital_user_obj.user.full_name = serializer.validated_data.get('name')
                hospital_user_obj.user.profile_pic_url = profile_pic_url
                hospital_user_obj.user.email = serializer.validated_data.get('email')
                hospital_user_obj.user.mobile = serializer.validated_data.get('phone')
                hospital_user_obj.user.password = make_password(serializer.validated_data.get('password'))
                hospital_user_obj.user.save()
                hospital_user_obj.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"You are not authorized to create hospital user"},status=status.HTTP_401_UNAUTHORIZED)
