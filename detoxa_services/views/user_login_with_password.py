from detoxa_backend import settings
from datetime import datetime, time, timedelta

from detoxa_services.models.hospitals_models import Hospital
from detoxa_services.models.organizations_models import Organizations
from ..models.users import Users, UserActiveTokens
from ..serializers.user_serializer import UserSignInWithPasswordSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from ..models.users import Users
from ..models.transactions_models import Transactions
from rest_framework import exceptions
from django.contrib.auth.hashers import make_password, check_password
from ..utils.generate_token import generate_access_token
from ..utils.user_authentication import UserAuthentication
from django.core.mail import send_mail


class UserSignInWithPassword(generics.GenericAPIView):
    authentication_classes = []
    serializer_class = UserSignInWithPasswordSerializer

    def post(self, request):
        user_sign_in_serializer = UserSignInWithPasswordSerializer(data=request.data)
        if user_sign_in_serializer.is_valid():
            email = user_sign_in_serializer.validated_data.get('email')
            password = user_sign_in_serializer.validated_data.get('password')
           
            if (email is None) or (password is None):
                raise exceptions.AuthenticationFailed('email and password required')

            user = Users.objects.filter(email=email).first()
           
            if user is None:
                raise exceptions.AuthenticationFailed('user not found')
            if not user.is_active:
                raise exceptions.AuthenticationFailed('User is currently inactive')

            if not (check_password(password, user.password)):
                raise exceptions.AuthenticationFailed('Email or password is wrong')

            serialized_user = UserSignInWithPasswordSerializer(user).data
            access_token = generate_access_token(user)
            UserActiveTokens.objects.create(user=user, user_token=access_token)

            # check for active subscription
            todays_date = datetime.today().date()
            subscription = Transactions.objects.filter(user=user,
                                                       subscription_end_date__gte=todays_date,
                                                       is_active=True).first()
            send_mail('Email for successful login', 'Logged in successfully ', settings.FROM_EMAIL, [user.email], fail_silently=False)

            if user.is_hospital_admin:   
                data = {
                    "success": True,
                    'Token': access_token,
                    'user': serialized_user,
                    'hospital': Hospital.objects.filter(user=user).values(),
                    'is_subscribed': True if subscription else False
                }
                return Response(data, status=status.HTTP_200_OK)
            elif user.is_society_admin:
                data = {
                    "success": True,
                    'Token': access_token,
                    'user': serialized_user,
                    'society': Organizations.objects.filter(user=user).values(),
                    'is_subscribed': True if subscription else False
                }
                return Response(data, status=status.HTTP_200_OK)
            elif user.is_school_admin:
                data = {
                    "success": True,
                    'Token': access_token,
                    'user': serialized_user,
                    'school': Organizations.objects.filter(user=user).values(),
                    'is_subscribed': True if subscription else False
                }
                return Response(data, status=status.HTTP_200_OK)
            elif user.is_company_admin:
                data = {
                    "success": True,
                    'Token': access_token,
                    'user': serialized_user,
                    'company': Organizations.objects.filter(user=user).values(),
                    'is_subscribed': True if subscription else False
                }
                return Response(data, status=status.HTTP_200_OK)
            elif user.is_doctor:
                data = {
                    "success": True,
                    'Token': access_token,
                    'user': serialized_user,
                    'is_subscribed': True if subscription else False
                }
                return Response(data, status=status.HTTP_200_OK)
            elif user.is_therapist:
                data = {
                    "success": True,
                    'Token': access_token,
                    'user': serialized_user,
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
                    try:
                        subscription = Transactions.objects.filter(user=user,
                                                            subscription_end_date__gte=todays_date,
                                                            is_active=True).first()
                    except Exception as e:
                        pass
                subscription = True if subscription else False
                data = {
                    "success": True,
                    'Token': access_token,
                    'user': serialized_user,
                    'is_subscribed': subscription
                }
                
                return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(user_sign_in_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSignOut(generics.GenericAPIView):

    def post(self, request):
        user = UserAuthentication.authenticate(self, request)[0]
    
        if not user:
            raise exceptions.AuthenticationFailed("User not found")
        user_token = request.headers.get('Authorization')
        if user_token:
            UserActiveTokens.objects.filter(user_token=user_token).delete()
            try:
                UserActiveTokens.objects.filter(user=user).delete()
            except:
                pass
            data = {
                "Success": True,
                "message": "User logged out successfully."
            }
            # send_mail('Email for logout', 'You have loggedout successfully ', settings.EMAIL_HOST_USER,[user.email], fail_silently=False)
            return Response(data, status=status.HTTP_200_OK)

        else:
            return Response({"Error": "User doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
