from botocore import exceptions
from detoxa_services.models.doctors import BankDetails
from detoxa_services.serializers.doctor_serializer import SaveBankDetailsSerializer
from detoxa_services.views.organizations_views import StandardResultsSetPagination
from ..models import Users
from ..models.therapy_session import TherapySession
from ..serializers.therapist_serializer import *
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from ..utils.user_authentication import UserAuthentication
import django_filters
import boto3
from ..models.therapist import Therapist
from django.contrib.auth.hashers import make_password


class GetAllTherapistCategory(generics.ListAPIView):
    authentication_classes = []
    serializer_class = GetTherapistCategorySerializer

    def get(self, request, *args, **kwargs):
        therapist_category_obj = TherapistCategory.objects.filter(is_active=True)
        data_list = []
        for category in therapist_category_obj:
            data = GetTherapistCategorySerializer(category).data
            data_list.append(data)
        return Response(data_list, status=status.HTTP_200_OK)


class DeleteTherapistCategory(generics.DestroyAPIView):
    authentication_classes = []

    def delete(self, request, *args, **kwargs):
        UserAuthentication.authenticate(self, request)[0]
        try:
            therapist_obj = TherapistCategory.objects.filter(id=self.kwargs['pk']).first()
            therapist_obj.is_active = False
            therapist_obj.save()

            data = {
                "success": True,
                "message": "Therapist Category deleted successfully"
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception:
            return Response({'message': f'Therapy session with id {kwargs["pk"]} does not exist', 'success': False}, status=status.HTTP_404_NOT_FOUND)





class CreateNewTherapist(generics.GenericAPIView):
    authentication_classes = []
    serializer_class = TherapistSerializer
    parser_classes = (MultiPartParser,)

    def post(self, request):
        user = UserAuthentication.authenticate(self, request)[0]
        therapist_serializer = TherapistSerializer(data=request.data)
        if not therapist_serializer.is_valid():
            return Response(therapist_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            name = therapist_serializer.validated_data.get('name')
            therapist_category = therapist_serializer.validated_data.get('therapist_category')
            degree_name = therapist_serializer.validated_data.get('degree_name')

            experience = therapist_serializer.validated_data.get('experience')
            email = therapist_serializer.validated_data.get('email')
            mobile = therapist_serializer.validated_data.get('mobile')

            password = therapist_serializer.validated_data.get('password')
            password = make_password(password)
            therapist_image = therapist_serializer.validated_data.get('therapist_image')

            time_slots = therapist_serializer.validated_data.get('therapist_time_slots')
            time_slots = ','.join(str(x) for x in time_slots)

            therapist_fee = therapist_serializer.validated_data.get('therapist_fee')
            is_active = therapist_serializer.validated_data.get('is_active')

            user = Users.objects.create(full_name=name, email=email, mobile=mobile, password=password, is_therapist=True)

            therapist_obj = Therapist.objects.create(user=user, name=name, therapist_category_id=therapist_category,
                                                     degree_name=degree_name, experience=experience,
                                                     therapist_time_slots=time_slots, therapist_fee=therapist_fee,
                                                     is_active=is_active)
            if therapist_image:
                try:
                    s3 = boto3.resource('s3', region_name='us-east-2',
                                        aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                        aws_secret_access_key='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')
                    s3.Bucket('detoxa').put_object(Key=therapist_serializer.validated_data.get('therapist_image').name,
                                                   Body=therapist_serializer.validated_data.get('therapist_image'),
                                                   ACL='public-read',
                                                   ContentType=therapist_serializer.validated_data.get('therapist_image').content_type, ContentDisposition='inline')

                    therapist_obj.therapist_image = f"https://detoxa.s3.us-east-2.amazonaws.com/{therapist_image.name}"
                    therapist_obj.save()
                except Exception as e:
                    print(e)

            therapist_obj_dict = {'id': therapist_obj.id}
            therapist_obj_dict.update(therapist_serializer.data)
            therapist_obj_dict['therapist_image'] = therapist_obj.therapist_image
            # therapist_obj_dict.update({'therapist_image': therapist_obj.therapist_image})

            data = {
                "success": True,
                'therapist': therapist_obj_dict
            }
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            raise e


class GetAllTherapistFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_by_name')
    therapist_category = django_filters.CharFilter(method='filter_by_therapist_category')
    experience = django_filters.CharFilter(method='filter_by_experience')

    class Meta:
        model = Therapist
        fields = []

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(name__icontains=value)

    def filter_by_therapist_category(self, queryset, name, value):
        return queryset.filter(therapist_category__name__icontains=value)

    def filter_by_experience(self, queryset, name, value):
        return queryset.filter(experience__iexact=value)


class GetAllTherapist(generics.ListAPIView):
    authentication_classes = []
    serializer_class = GetTherapistSerializer
    filterset_class = GetAllTherapistFilter
    pagination_class = StandardResultsSetPagination

    def get(self, request, *args, **kwargs):
        # user = UserAuthentication.authenticate(self, request)[0]
        therapist_obj = Therapist.objects.filter(is_active=True).order_by("-id")
        therapist_obj = GetAllTherapistFilter(request.GET, queryset=therapist_obj).qs.distinct()
        data_list = []
        total_count = Therapist.objects.filter(is_active=True).count()
        for therapist in therapist_obj:
            data = GetTherapistSerializer(therapist).data
            data['therapist_category'] = therapist.therapist_category.name
            data_list.append(data)
        therapist_data = self.paginate_queryset(data_list)
        return Response({'data': therapist_data, 'count': total_count}, status=status.HTTP_200_OK)


class CreateTherapyCategory(generics.CreateAPIView):
    authentication_classes = []
    serializer_class = TherapistCategorySerializer
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        UserAuthentication.authenticate(self, request)[0]
        category_serializer = TherapistCategorySerializer(data=request.data)
        if category_serializer.is_valid():
            name = category_serializer.validated_data.get('name')
            therapist_image = category_serializer.validated_data.get('therapist_image')
            category_obj = TherapistCategory.objects.create(name=name)
            if therapist_image:
                try:
                    s3 = boto3.resource('s3', region_name='us-east-2',
                                        aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                        aws_secret_access_key='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')
                    s3.Bucket('detoxa').put_object(Key=category_serializer.validated_data.get('therapist_image').name,
                                                   Body=category_serializer.validated_data.get('therapist_image'),
                                                   ACL='public-read',
                                                   ContentType=category_serializer.validated_data.get('therapist_image').content_type, ContentDisposition='inline')

                    category_obj.therapist_image = f"https://detoxa.s3.us-east-2.amazonaws.com/{therapist_image.name}"
                    category_obj.save()
                except Exception as e:
                    print(e)

            category_obj_dict = {'id': category_obj.id, 'name': category_obj.name}
            category_obj_dict.update(category_serializer.data)

            category_obj_dict.update({'therapist_image': category_obj.therapist_image})
            # category_obj_dict['therapist_image'] = category_obj.therapist_image

            data = {
                "success": True,
                'data': category_obj_dict
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTherapistById(generics.ListAPIView):
    authentication_classes = []
    serializer_class = GetTherapistSerializer

    def get(self, request, *args, **kwargs):
        user = UserAuthentication.authenticate(self, request)[0]
        if therapist_obj := Therapist.objects.filter(id=kwargs['pk']).first():
        # if therapist_obj:
            data = GetTherapistSerializer(therapist_obj).data
            data['therapist_category'] = therapist_obj.therapist_category.name
            try:
                bank_details = BankDetails.objects.filter(user=therapist_obj.user).first()
            except:
                bank_details = None
            data['bank_details'] = SaveBankDetailsSerializer(bank_details,many=False).data
            
            data = {
                "success": True,
                "data": data
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            raise exceptions.NotFound('Therapist not found')


class DeleteTherapist(generics.DestroyAPIView):
    authentication_classes = []
    serializer_class = GetTherapistSerializer

    def delete(self, request, *args, **kwargs):
        UserAuthentication.authenticate(self, request)[0]
        if TherapySession.objects.filter(therapist__id=kwargs['pk'],status='Pending').exists():
            return Response({"msg": "This Therapist cannot be deleted. Therapist is associated with one or more appointments"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if therapist_obj := Therapist.objects.filter(id=kwargs['pk']).first():
                therapist_obj.is_active = False
                therapist_obj.save()

                data = {
                    "success": True,
                    "message": "Therapist deleted successfully"
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                raise exceptions.NotFound('Therapist not found.')


class UpdateTherapistDetails(generics.UpdateAPIView):
    serializer_class = UpdateTherapistSerializer
    parser_classes = (MultiPartParser,)

    def put(self, request, *args, **kwargs):
        therapist_obj = Therapist.objects.get(id=kwargs.get('pk'))
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        try:
            if logged_in_user.is_admin:
                serializer = UpdateTherapistSerializer(data=request.data)
                if serializer.is_valid():
                    profile_pic = serializer.validated_data.get('profile_pic')
                    profile_pic_url = ''
                    if profile_pic:
                        try:
                            s3 = boto3.resource('s3', region_name='us-east-2',
                                                aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                                aws_secret_access_key='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')
                            s3.Bucket('detoxa').put_object(Key=profile_pic.name, Body=profile_pic, ACL='public-read',
                                                           ContentType=profile_pic.content_type,
                                                           ContentDisposition='inline')
                            profile_pic_url = f"https://detoxa.s3.us-east-2.amazonaws.com/{profile_pic.name}"
                        except Exception as e:
                            print(e)
                    therapist_obj.user.full_name = serializer.validated_data.get('name')
                    therapist_obj.name = serializer.validated_data.get('name')
                    therapist_obj.therapist_category = TherapistCategory.objects.get(id=serializer.validated_data.get('therapist_category'))
                    therapist_obj.degree_name = serializer.validated_data.get('degree_name')
                    therapist_obj.therapist_fee = serializer.validated_data.get('therapist_fee')
                    therapist_obj.therapist_time_slots = serializer.validated_data.get('therapist_time_slots')
                    therapist_obj.experience = serializer.validated_data.get('experience')
                    therapist_obj.therapist_image_url = profile_pic_url
                    therapist_obj.user.profile_pic_url = profile_pic_url
                    therapist_obj.user.email = serializer.validated_data.get('email')
                    therapist_obj.user.mobile = serializer.validated_data.get('phone')
                    therapist_obj.user.password = make_password(serializer.validated_data.get('password'))
                    therapist_obj.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "You are not authorized to create therapist"}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            print(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)