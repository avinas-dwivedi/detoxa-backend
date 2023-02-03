from asyncio.log import logger
import email
import boto3
import secrets
import string
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.conf import settings
from django.db.models import query
from detoxa_services.models import appointments_models
from detoxa_services.models.doctors import Doctors
from detoxa_services.models.hospitals_models import Hospital
from detoxa_services.models.notification_models import UserDatabaseForNotification
from detoxa_services.models.organizations_models import Organizations
from detoxa_services.utils.generate_otp import generateMobileOTP, verifyMobileOTP
from detoxa_services.views.organizations_views import StandardResultsSetPagination
from .whatsapp import whatsapp_notification
from ..serializers.user_serializer import UserForgotPasswordSerializer, UserSignupCreateOTPSerializer, UserSignupSerializer, AdminSignupSerializer, UserUpdatePasswordSerializer,UserUpdateSerializer,UserSerializer
from rest_framework import authentication, generics, serializers, status
from detoxa_services.utils.user_authentication import UserAuthentication
from rest_framework.parsers import MultiPartParser
from django.core.mail import send_mail

from rest_framework.response import Response
from rest_framework import exceptions
from ..models.users import Users, UserActiveTokens
from django.contrib.auth.hashers import make_password,check_password
from ..utils.generate_token import generate_access_token


def generate_random_password():
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits)for i in range(8))


class UserRegistrationCreateOTP(generics.CreateAPIView):
    serializer_class = UserSignupCreateOTPSerializer
    queryset = Users.objects.all()
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        new_user = UserSignupCreateOTPSerializer(data=request.data)
        if new_user.is_valid():
            try:
                full_name = new_user.validated_data.get('full_name')
                session_id = new_user.validated_data.get('session_id')
                otp = new_user.validated_data.get('otp')
                mobile = new_user.validated_data.get('mobile')
                email = new_user.validated_data.get('email')
                password = new_user.validated_data.get('password')
                is_tnc_accepted = new_user.validated_data.get('is_tnc_accepted')
                password = make_password(password)
                email_exist = Users.objects.filter(email=email).first()
                mobile_exist = Users.objects.filter(mobile=mobile).first()
                if email_exist:
                    raise exceptions.AuthenticationFailed('Email already exist')
                if mobile_exist:
                    raise exceptions.AuthenticationFailed('Mobile already exist')
                otp_generation = generateMobileOTP(mobile)
                print('----',type(otp_generation),otp_generation)
                if request.META['HTTP_HOST'] == '127.0.0.1:8000':
                    if otp_generation['Status'] == 'Success':
                        # user = Users.objects.create(full_name=full_name, mobile=mobile, email=email, password=password, is_tnc_accepted=is_tnc_accepted)
                        # user_data = {
                        #     'full_name': user.full_name,
                        #     'email': user.email,
                        #     'mobile': user.mobile,
                        #     'is_active': user.is_active,
                        #     'is_admin': user.is_admin,
                        #     'is_tnc_accepted':user.is_tnc_accepted
                        # }
                        # access_token = generate_access_token(user)
                        data = {
                            "success": True,
                            "otp":otp_generation,
                            "message":"OTP sent successfully"
                        }
                        logger.info("OTP sent successfully")
                        return Response(data, status=status.HTTP_201_CREATED)
                    else:
                        logger.error("OTP not sent",otp_generation)
                        raise exceptions.ValidationError(otp_generation.json())
                else:
                    if otp_generation['Status'] == 'Success':
                        data = {
                            "success": True,
                            "otp":otp_generation,
                            "message":"OTP sent successfully"
                        }
                        logger.info("OTP sent successfully")
                        return Response(data, status=status.HTTP_201_CREATED)
                    else:
                        logger.error("OTP not sent",otp_generation)
                        raise exceptions.ValidationError(otp_generation.json())
            except Exception as e:
                logger.error("OTP not sent exception",e)
                raise e
        else:
            logger.error("OTP not sent exception",new_user.errors)
            return Response(new_user.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRegistration(generics.CreateAPIView):
    serializer_class = UserSignupSerializer
    queryset = Users.objects.all()
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        new_user = UserSignupSerializer(data=request.data)
        if new_user.is_valid():
            try:
                full_name = new_user.validated_data.get('full_name')
                session_id = new_user.validated_data.get('session_id')
                otp = new_user.validated_data.get('otp')
                mobile = new_user.validated_data.get('mobile')
                email = new_user.validated_data.get('email')
                password = new_user.validated_data.get('password')
                is_tnc_accepted = new_user.validated_data.get('is_tnc_accepted')
                password = make_password(password)
                email_exist = Users.objects.filter(email=email).first()
                mobile_exist = Users.objects.filter(mobile=mobile).first()
                if email_exist:
                    raise exceptions.AuthenticationFailed('Email already exist')
                if mobile_exist:
                    raise exceptions.AuthenticationFailed('Mobile already exist')
                otp_verfication_status = verifyMobileOTP(session_id,otp)
                if otp_verfication_status == 200:
                    user = Users.objects.create(full_name=full_name, mobile=mobile, email=email, password=password, is_tnc_accepted=is_tnc_accepted)
                    UserDatabaseForNotification.objects.create(name=user.full_name, phone_number=user.mobile, email=user.email)
                    user_data = {
                        'full_name': user.full_name,
                        'email': user.email,
                        'mobile': user.mobile,
                        'is_active': user.is_active,
                        'is_admin': user.is_admin,
                        'is_tnc_accepted':user.is_tnc_accepted
                    }
                    access_token = generate_access_token(user)
                    data = {
                        "success": True,
                        'Token': access_token,
                        'User': user_data,
                        'is_subscribed': False
                    }
                    whatsapp_notification(mobile, 'Welcome Deleted Servies Registration successful')
                    send_mail('Email for registration', 'User Registration successful for detoxa', settings.FROM_EMAIL,[user.email], fail_silently=False)
                    logger.info("User registered successfully")
                    return Response(data, status=status.HTTP_201_CREATED)
                else:
                    raise exceptions.ValidationError(('Invalid Otp'))
            except Exception as e:
                logger.error("User registration exception",e)
                raise e
        else:
            logger.error("User registration exception",new_user.errors)
            return Response(new_user.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminRegistration(generics.CreateAPIView):
    serializer_class = AdminSignupSerializer
    queryset = Users.objects.all()
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        new_user = AdminSignupSerializer(data=request.data)
        if new_user.is_valid():
            try:
                full_name = new_user.validated_data.get('full_name')
                mobile = new_user.validated_data.get('mobile')
                email = new_user.validated_data.get('email')
                password = new_user.validated_data.get('password')
                password = make_password(password)
                email_exist = Users.objects.filter(email=email).first()
                mobile_exist = Users.objects.filter(mobile=mobile).first()
                if email_exist:
                    raise exceptions.AuthenticationFailed('Email already exist')
                if mobile_exist:
                    raise exceptions.AuthenticationFailed('Mobile already exist')
                user = Users.objects.create(full_name=full_name, mobile=mobile, email=email, password=password, is_admin=True)
                user_data = {
                    'full_name': user.full_name,
                    'email': user.email,
                    'mobile': user.mobile,
                    'is_active': user.is_active,
                    'is_admin': user.is_admin
                }
                access_token = generate_access_token(user)
                UserActiveTokens.objects.create(user=user, user_token=access_token)
                data = {
                    "success": True,
                    'Token': access_token,
                    'User': user_data
                }
                return Response(data, status=status.HTTP_201_CREATED)
            except Exception as e:
                raise e
        else:
            return Response(new_user.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUser(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    queryset = Users.objects.all()
    authentication_classes = []
    parser_classes = [MultiPartParser]

    def put(self, request, *args, **kwargs):
        data = request.data
        serializer = UserUpdateSerializer(data=data)
        if serializer.is_valid():
            user_obj = Users.objects.get(id=kwargs.get('pk'))
            user_obj.address = serializer.validated_data.get('address')
            profile_pic = serializer.validated_data.get('profile_pic')
            if profile_pic:
                s3 = boto3.resource('s3', region_name='us-east-2',
                                            aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                            aws_secret_access_key='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')
                s3.Bucket('detoxa').put_object(Key=profile_pic.name, Body=profile_pic, ACL='public-read',
                                                       ContentType=profile_pic.content_type, ContentDisposition='inline')
                user_obj.profile_pic_url=f"https://detoxa.s3.us-east-2.amazonaws.com/{profile_pic.name}"
            # user_obj.mobile = serializer.validated_data.get('mobile')
            # user_obj.email = serializer.validated_data.get('email')
            # user_obj.is_tnc_accepted = serializer.validated_data.get('is_tnc_accepted')
            user_obj.save()
            return Response({"success": True,'msg':'User details updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'success':False,'errors':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})

class ChangePasswordAPIView(generics.UpdateAPIView):
    serializer_class = UserUpdatePasswordSerializer
    queryset = Users.objects.all()
    authentication_classes = []

    def put(self, request, *args, **kwargs):
        data = request.data
        serializer = UserUpdatePasswordSerializer(data=data)
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        if logged_in_user:
            if serializer.is_valid():
                user_obj = Users.objects.get(id=kwargs.get('pk'))
                old_password = serializer.validated_data.get('old_password')
                new_password = serializer.validated_data.get('new_password')
                confirm_new_password = serializer.validated_data.get('confirm_new_password')
                if not (check_password(old_password,user_obj.password)):
                    return Response({'success':False,'errors':'Old password is incorrect', 'status':status.HTTP_400_BAD_REQUEST})
                if new_password != confirm_new_password:
                    return Response({'success':False,'errors':'New password and confirm password does not match', 'status':status.HTTP_400_BAD_REQUEST})
                if check_password(old_password,user_obj.password) and new_password == confirm_new_password:
                    user_obj.password = make_password(new_password)
                    user_obj.save()
                    return Response({"success": True,'msg':'Password updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'success':False,'errors':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})
        else:
            return Response({'success':False,'errors':'Log in to change password', 'status':status.HTTP_400_BAD_REQUEST})


class UserForgotPassword(generics.CreateAPIView):
    authentication_classes = []
    serializer_class = UserForgotPasswordSerializer


    def post(self,request,*args,**kwargs):
        serializer = UserForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            try:
                user_obj = Users.objects.get(email=email)
                random_string = generate_random_password()
                password = make_password(random_string)
                user_obj.password = password
                user_obj.save()
                send_mail('Email for reset password on detoxa', f'New password : {random_string}. Use this password to login and change your password after logging in successfully', settings.FROM_EMAIL,[user_obj.email], fail_silently=False)
                return Response({"success": True,'msg':'New password sent successfully on registered email id'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'success':False,'errors':'Email does not exist', 'status':status.HTTP_400_BAD_REQUEST})
        else:
            return Response({'success':False,'errors':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})


class DeleteUser(generics.DestroyAPIView):
    queryset = Users.objects.all()
    authentication_classes = []

    def delete(self, request, *args, **kwargs):
        user_obj = Users.objects.get(id=kwargs.get('pk'))
        appointments = appointments_models.Appointment.objects.filter(user=user_obj)
        try:
            doctor_obj = Doctors.objects.get(user=user_obj)
            doctor_obj.delete()
        except:
            pass
        try:
            hospital_obj = Hospital.objects.get(user=user_obj)
            hospital_obj.delete()
        except:
            pass
        try:
            organization_obj = Organizations.objects.filter(user=user_obj)
            for organization in organization_obj:
                organization.delete()
        except:
            pass
        try:
            for appointment in appointments:
                appointment.delete()
        except:
            pass
        
        user_obj.delete()

        return Response({'success':True,'msg':'User deleted successfully'}, status=status.HTTP_200_OK)

class GetUsersAPIView(generics.GenericAPIView):
    authentication_classes = []
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination

    mobile = openapi.Parameter(
        'state', openapi.IN_QUERY, description="User mobile to  be passed to get the list of users based on their mobile number.", required=False, type=openapi.TYPE_STRING)
    email = openapi.Parameter(
        'email', openapi.IN_QUERY, description="User email to  be passed to get the list of users based on their email.", required=False, type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[mobile, email])
    def get(self, request, *args, **kwargs):
        mobile = request.query_params.get('mobile')
        email = request.query_params.get('email')
        if mobile and not email:
            users = Users.objects.filter(is_admin=False,is_doctor=False,is_therapist=False,is_school_admin=False,is_society_admin=False,is_company_admin=False,is_hospital_admin=False,mobile__icontains=mobile)
            page = self.paginate_queryset(users)
            serializer = UserSerializer(page, many=True)
            return Response({'success':True,'data':serializer.data}, status=status.HTTP_200_OK)
        if email and not mobile:
            users = Users.objects.filter(is_admin=False,is_doctor=False,is_therapist=False,is_school_admin=False,is_society_admin=False,is_company_admin=False,is_hospital_admin=False,email__icontains=email)
            page = self.paginate_queryset(users)
            serializer = UserSerializer(page, many=True)
            return Response({'success':True,'data':serializer.data}, status=status.HTTP_200_OK)
        if mobile and email:
            users = Users.objects.filter(is_admin=False,is_doctor=False,is_therapist=False,is_school_admin=False,is_society_admin=False,is_company_admin=False,is_hospital_admin=False,mobile__icontains=mobile,email__icontains=email)
            page = self.paginate_queryset(users)
            serializer = UserSerializer(page, many=True)
            return Response({'success':True,'data':serializer.data}, status=status.HTTP_200_OK)
        users = Users.objects.filter(is_admin=False,is_doctor=False,is_therapist=False,is_school_admin=False,is_society_admin=False,is_company_admin=False,is_hospital_admin=False)
        page = self.paginate_queryset(users)
        serializer = UserSerializer(page, many=True)
        return Response({'success':True,'data':serializer.data}, status=status.HTTP_200_OK)
