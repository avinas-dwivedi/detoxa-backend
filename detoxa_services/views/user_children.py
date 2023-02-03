import logging
import boto3
from datetime import datetime, time, timedelta
from rest_framework.serializers import Serializer
from ..serializers.user_child_relation import *
from rest_framework.response import Response
from ..utils.user_authentication import UserAuthentication
from django.utils.translation import ugettext_lazy as _
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from ..models.users import Users
from ..models.transactions_models import Transactions
from ..models.user_child_relation import UserChildRelation
from detoxa_backend import settings
from botocore.exceptions import ClientError
from ..utils.helper_functions import unique_s3_key
from rest_framework.parsers import MultiPartParser


class AddChildUser(generics.GenericAPIView):
    authentication_class = []
    serializer_class = AddChildUserSerializer
    parser_classes = (MultiPartParser,)

    def post(self, request):
        serialized = AddChildUserSerializer(data=request.data)
        if serialized.is_valid():
            logged_in_user = UserAuthentication.authenticate(self, request)[0]
            image = serialized.validated_data.get('picture_url')
            # relation = serialized.validated_data.get('relation')
            full_name = serialized.validated_data.get('full_name')
            dob = serialized.validated_data.get('dob')
            gender = serialized.validated_data.get('gender')
            email = serialized.validated_data.get('email')
            age = serialized.validated_data.get('age')
            # filename = picture_url.name
            if email:
                email = email.lower()
            if email and Users.objects.filter(email=email).count() > 0:
                raise ValidationError(_('Email already exists'))

            # Check for duplicity
            duplicate_users = Users.objects.filter(full_name__iexact=full_name, dob=dob)
            if duplicate_users:
                user_relation = UserChildRelation.objects.filter(primary_user=logged_in_user,
                                                                 family_member__in=duplicate_users, is_active=True)
                if user_relation:
                    raise ValidationError(_('Child User already added'))
                
            profile_pic_url = None
            try:
                s3 = boto3.resource('s3', region_name='us-east-2',
                                    aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                    aws_secret_access_key='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')
                s3.Bucket('detoxa').put_object(Key=image.name, Body=image)
                profile_pic_url = f"https://detoxa.s3.us-east-2.amazonaws.com/{image.name}"
            except Exception as e:
                print(e)

            new_user = Users.objects.create(full_name=full_name, dob=dob, gender=gender,
                                            email=email, age=age, is_tnc_accepted=True, profile_pic_url=profile_pic_url)

            UserChildRelation.objects.create(parent_user=logged_in_user, child_user=new_user)

            data = {
                "success": True,
                "data": "Child user has been added."
            }
            return Response(data, status=status.HTTP_201_CREATED)

        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        serializer_class = UserSerializer
        user_children = UserChildRelation.objects.filter(parent_user=logged_in_user, is_active=True)
        child_list = list()
        subscription_dict = {}
        for obj in user_children:
            child_json = {"id": obj.child_user.id, "full_name": obj.child_user.full_name, "age": obj.child_user.age,
                          "gender": obj.child_user.gender, 'active': obj.is_active,
                          "dob": obj.child_user.dob, 'profile_pic_url': obj.child_user.profile_pic_url}

            child_list.append(child_json)
            todays_date = datetime.today().date()

            # check for active subscription
            subscription = Transactions.objects.filter(user=logged_in_user,
                                                       subscription_end_date__gte=todays_date,
                                                       is_active=True).first()
            if subscription:
                subscription_type = subscription.subscription_type
                renewal_date = subscription.subscription_end_date + timedelta(days=1)
                renewal_date = datetime.strftime(renewal_date, "%d/%m/%Y %I:%M %p")
                if subscription.tenure == '1':
                    membership = "Monthly"
                elif subscription.tenure == '6':
                    membership = "Half Yearly"
                else:
                    membership = "Yearly"
                subscription_dict = {"subscription_type": subscription_type,
                                     "renewal_date": renewal_date,
                                     "membership": membership}
        json_output = {"success": True, 'data': child_list, 'my_details': serializer_class(logged_in_user).data,
                       "subscription_data": subscription_dict}
        return Response(json_output, status=status.HTTP_200_OK)


class UpdateUserChild(generics.UpdateAPIView):
    serializer_class = AddChildUserSerializer
    model = UserChildRelation

    def put(self, request, *args, **kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        try:
            user_child = UserChildRelation.objects.get(child_user=kwargs.get('pk'), parent_user=logged_in_user)
            serialized = UpdateChildUserSerializer(data=request.data)
            if serialized.is_valid():
                # user_child.relation = serialized.validated_data.get('relation')
                user_child.child_user.full_name = serialized.validated_data.get('full_name')
                user_child.child_user.dob = serialized.validated_data.get('dob')
                user_child.child_user.gender = serialized.validated_data.get('gender')
                # user_child.child_user.email = serialized.validated_data.get('email')
                user_child.child_user.age = serialized.validated_data.get('age')
                image = serialized.validated_data.get('picture_url')
                if image:
                    try:
                        s3 = boto3.resource('s3', region_name='us-east-2',
                                            aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                            aws_secret_access_key='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')
                        s3.Bucket('detoxa').put_object(Key=image.name, Body=image)
                        user_child.child_user.profile_pic_url = f"https://detoxa.s3.us-east-2.amazonaws.com/{image.name}"
                    except Exception as e:
                        print(e)
                user_child.save()
                user_child.child_user.save()

                data = {
                    "success": True,
                    "data": "Child user has been updated."
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print('Exception--', e)
            data = {
                "success": False,
                "data": str(e)
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class DeleteUserChild(generics.DestroyAPIView):

    def delete(self, request, *args, **kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        try:
            user_child = UserChildRelation.objects.get(child_user=kwargs.get('pk'), parent_user=logged_in_user)
            # user_child.is_active = False
            # user_child.save()
            user_child.delete()
            data = {
                "success": True,
                "data": "Child user has been removed."
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            data = {
                "success": False,
                "data": "Child user not found."
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class GetChildrenDetails(generics.RetrieveAPIView):
    serializer_class = ChildDetailsSerializer

    def get(self, request, *args, **kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        try:
            child = UserChildRelation.objects.get(id=kwargs.get('pk'), parent_user=logged_in_user)
            serializer = ChildDetailsSerializer(child, many=False)
            return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status.HTTP_400_BAD_REQUEST)
