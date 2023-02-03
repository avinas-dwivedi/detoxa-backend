from asyncio.log import logger
from detoxa_services.models.hospitals_models import Hospital
from detoxa_services.models.organizations_models import Organizations
from ..models.users import Users
from datetime import datetime, time, timedelta
from ..serializers.user_serializer import UserGenerateSignInOTPSerializer, UserSignInWithOTPSerializer, UserSignInWithPasswordSerializer, UserSignupCreateOTPSerializer, UserSignupSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from ..models.users import Users
from ..models.transactions_models import Transactions
from rest_framework import exceptions
from django.contrib.auth.hashers import make_password, check_password
from ..utils.generate_token import generate_access_token
from ..utils.generate_otp import generateMobileOTP, verifyMobileOTP
from rest_framework.exceptions import ValidationError
from ..models.mobile_otp import MobileOTP
from ..constants import constants
from datetime import datetime, timedelta


class GenerateSignInOTP(generics.GenericAPIView):
    authentication_classes = []
    serializer_class = UserGenerateSignInOTPSerializer

    def post(self, request):
        user_sign_in_otp_serializer = UserGenerateSignInOTPSerializer(data=request.data)
        data = {}
        if user_sign_in_otp_serializer.is_valid():
            mobile = user_sign_in_otp_serializer.validated_data.get('mobile_no')
            try:
                user = Users.objects.get(mobile=mobile)
                otp = generateMobileOTP(mobile)
                # MobileOTP.objects.filter(mobile_no=mobile).delete()
                # MobileOTP.objects.create(mobile_no=mobile, otp=otp)
                if not user.is_active:
                    raise ValidationError(('User is currently inactive'))
                data["mobile_no"] = mobile
                data['otp'] = otp
                data["message"] = "OTP sent successfully"
                return Response(data, status=status.HTTP_200_OK)
            except Users.DoesNotExist:
                raise ValidationError(('Mobile Number not Registered'))
        else:
            return Response(user_sign_in_otp_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSignInWithOTP(generics.GenericAPIView):
    authentication_classes = []
    serializer_class = UserSignInWithOTPSerializer

    def post(self, request):
        print(request.data)
        user_sign_in_serializer = UserSignInWithOTPSerializer(data=request.data)
        if user_sign_in_serializer.is_valid():
            mobile = user_sign_in_serializer.validated_data.get('mobile')
            session_id = user_sign_in_serializer.validated_data.get('session_id')
            otp = user_sign_in_serializer.validated_data.get('otp')
            try:
                user = Users.objects.get(mobile=mobile)
                serialized_user = UserSignInWithPasswordSerializer(user).data
                if not user.is_active:
                    raise ValidationError(('User is currently inactive'))
                # mobile_otps = MobileOTP.objects.filter(mobile_no=mobile).order_by('-updated')
                # mobile_otp = mobile_otps.first()
                # check for active subscription
                # import ipdb
                # ipdb.set_trace()
                todays_date = datetime.today().date()
                subscription = Transactions.objects.filter(user=user,
                                                           subscription_end_date__gte=todays_date,
                                                           is_active=True).first()
                # if not mobile_otp:
                #     raise ValidationError(('Failed to generate OTP for this mobile number'))
                # generated_otp = mobile_otp.otp
                # if str(otp) == str(generated_otp):
                #     mobile_otps.delete()
                otp_verfication_status = verifyMobileOTP(session_id,otp)
                logger.info('-------',otp_verfication_status)
                if otp_verfication_status == 200:
                    access_token = generate_access_token(user)
                    user = UserSignupCreateOTPSerializer(user).data
                    # data = {
                    #     "success": True,
                    #     'Token': access_token,
                    #     'user': serialized_user,
                    #     'is_subscribed': True if subscription else False
                    # }
                    if user['is_hospital_admin']:   
                        data = {
                            "success": True,
                            'Token': access_token,
                            'user': user,
                            'hospital': Hospital.objects.filter(user__id=user['id']).values(),
                            'is_subscribed': True if subscription else False
                        }
                        return Response(data, status=status.HTTP_200_OK)
                    elif user['is_society_admin']:
                        data = {
                            "success": True,
                            'Token': access_token,
                            'user': user,
                            'society': Organizations.objects.filter(user__id=user['id']).values(),
                            'is_subscribed': True if subscription else False
                        }
                        return Response(data, status=status.HTTP_200_OK)
                    elif user['is_school_admin']:
                        data = {
                            "success": True,
                            'Token': access_token,
                            'user': user,
                            'school': Organizations.objects.filter(user__id=user['id']).values(),
                            'is_subscribed': True if subscription else False
                        }
                        return Response(data, status=status.HTTP_200_OK)
                    elif user['is_company_admin']:
                        data = {
                            "success": True,
                            'Token': access_token,
                            'user': user,
                            'company': Organizations.objects.filter(user__id=user['id']).values(),
                            'is_subscribed': True if subscription else False
                        }
                        return Response(data, status=status.HTTP_200_OK)
                    elif user['is_doctor']:
                        data = {
                            "success": True,
                            'Token': access_token,
                            'user': user,
                            'is_subscribed': True if subscription else False
                        }
                        return Response(data, status=status.HTTP_200_OK)
                    else:
                        subscription = None
                        try:
                            organization = Organizations.objects.filter(user=user).first()
                            subscription = Transactions.objects.filter(user=organization.user,
                                                                subscription_end_date__gte=todays_date,
                                                                is_active=True).first()
                        except Exception as e:
                            subscription = True if subscription else False
                        data = {
                            "success": True,
                            'Token': access_token,
                            'user': user,
                            'is_subscribed': subscription
                        }
                        logger.info("User Sign In Successfully")
                        # send_mail('Email for successful login', 'Logged in successfully ', settings.FROM_EMAIL,['ravichoudhary766@gmail.com'], fail_silently=False)
                        return Response(data, status=status.HTTP_200_OK)
                else:
                    logger.error("User Sign In Failed")
                    return  Response({'msg':'Invalid Otp'}, status=status.HTTP_400_BAD_REQUEST)
            except Users.DoesNotExist:
                logger.error("User Sign In Failed")
                return  Response({'msg':'Mobile Number not Registered'},status=status.HTTP_400_BAD_REQUEST)
        else:
            print(user_sign_in_serializer.errors)
            logger.error("User Sign In Failed")
            return Response({'msg':user_sign_in_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
