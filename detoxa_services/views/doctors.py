import datetime
from email.policy import HTTP
import uuid
from detoxa_services.models import therapist
from detoxa_services.models.appointments_models import Appointment
from detoxa_services.models.favourites import Favourites
from detoxa_services.models.notification_models import UserDatabaseForNotification
from detoxa_services.models.therapy_session import TherapySession
from detoxa_services.serializers.favourite_serializer import FavouritesSerializer
from detoxa_services.views import appointments

from detoxa_services.views.organizations_views import StandardResultsSetPagination
from django.db.models import Sum
from ..models import Users
from ..serializers.doctor_serializer import *
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from ..utils.user_authentication import UserAuthentication
from detoxa_backend import settings
from botocore.exceptions import ClientError
from ..utils.helper_functions import unique_s3_key
import django_filters
import logging
import boto3
from ..models.doctors import BankDetails, Doctors
from ..serializers.doctor_serializer import Specialization, GetAllDoctorsSerializer, DoctorSerializer, GetAllSpecializationSerializer
from django.contrib.auth.hashers import make_password


class CreateNewDoctors(generics.GenericAPIView):
    authentication_classes = []
    serializer_class = DoctorSerializer
    parser_classes = (MultiPartParser,)

    def post(self, request):
        user = UserAuthentication.authenticate(self, request)[0]
        doctor_serializer = DoctorSerializer(data=request.data)
        if doctor_serializer.is_valid():
            try:
                name = doctor_serializer.validated_data.get('name')
                specialization = doctor_serializer.validated_data.get('specialization')
                degree_name = doctor_serializer.validated_data.get('degree_name')

                experience = doctor_serializer.validated_data.get('experience')
                email = doctor_serializer.validated_data.get('email')
                mobile = doctor_serializer.validated_data.get('mobile')
                password = doctor_serializer.validated_data.get('password')

                doc_image = doctor_serializer.validated_data.get('doc_image')
                password = make_password(password)
                time_slots = doctor_serializer.validated_data.get('time_slots')
                time_slots = ','.join(str(x) for x in time_slots)

                consultation_fee = doctor_serializer.validated_data.get('consultation_fee')
                is_active = doctor_serializer.validated_data.get('is_active')

                user = Users.objects.create(full_name=name, email=email, mobile=mobile, password=password, is_doctor=True)
                UserDatabaseForNotification.objects.create(name=user.full_name, phone_number=user.mobile, email=user.email)

                doctor_obj = Doctors.objects.create(user=user, name=name, specialization_id=specialization,
                                                    degree_name=degree_name, experience=experience,
                                                    time_slots=time_slots, consultation_fee=consultation_fee,
                                                    is_active=is_active
                                                    )
                if doc_image:
                    try:
                        s3 = boto3.resource('s3', region_name='us-east-2',
                                            aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                            aws_secret_access_key='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')
                        s3.Bucket('detoxa').put_object(Key=doctor_serializer.validated_data.get('doc_image').name,
                                                       Body=doctor_serializer.validated_data.get('doc_image'),
                                                       ACL='public-read',
                                                       ContentType=doctor_serializer.validated_data.get('doc_image').content_type, ContentDisposition='inline')

                        doctor_obj.doc_image = f"https://detoxa.s3.us-east-2.amazonaws.com/{doc_image.name}"
                        doctor_obj.save()
                    except Exception as e:
                        print(e)

                doctor_obj_dict = {'id': doctor_obj.id}
                doctor_obj_dict.update(doctor_serializer.data)
                doctor_obj_dict.update({'doc_image': doctor_obj.doc_image})

                data = {
                    "success": True,
                    'doctor': doctor_obj_dict
                }
                return Response(data, status=status.HTTP_201_CREATED)
            except Exception as e:
                raise e
        else:
            return Response(doctor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateDoctorDetails(generics.UpdateAPIView):
    serializer_class = UpdateDoctorsSerializer
    parser_classes = (MultiPartParser,)

    def put(self, request, *args, **kwargs):
        doctor_obj = Doctors.objects.get(id=kwargs.get('pk'))
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        try:
            if logged_in_user.is_admin or logged_in_user.is_doctor:
                serializer = UpdateDoctorsSerializer(data=request.data)
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

                    name = serializer.validated_data.get('name')
                    email = serializer.validated_data.get('email')
                    mobile = serializer.validated_data.get('phone')
                    password = serializer.validated_data.get('password')

                    user = Users.objects.filter(pk=doctor_obj.user_id).update(full_name=name, email=email,
                                                                       mobile=mobile, password=make_password(password),
                                                                       is_doctor=True)

                    doctor_obj.name = serializer.validated_data.get('name')
                    doctor_obj.specialization = Specialization.objects.get(id=serializer.validated_data.get('specialization'))
                    doctor_obj.degree_name = serializer.validated_data.get('degree_name')

                    doctor_obj.consultation_fee = serializer.validated_data.get('consultation_fee')
                    # doctor_obj.time_slots = serializer.validated_data.get('time_slots')

                    time_slots = serializer.validated_data.get('time_slots')
                    time_slots = ','.join(str(x) for x in time_slots)
                    doctor_obj.time_slots = time_slots

                    doctor_obj.experience = serializer.validated_data.get('experience')
                    doctor_obj.doc_image_url = profile_pic_url
                    doctor_obj.user_id = doctor_obj.user_id
                    # doctor_obj.user.full_name = serializer.validated_data.get('name')
                    # doctor_obj.user.profile_pic_url = profile_pic_url
                    # doctor_obj.user.email = serializer.validated_data.get('email')
                    # doctor_obj.user.mobile = serializer.validated_data.get('phone')
                    # doctor_obj.user.password = make_password(serializer.validated_data.get('password'))
                    doctor_obj.save()

                    return Response(serializer.data, status=status.HTTP_201_CREATED)

                return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "You are not authorized to create hospital user"}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            print(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    # def put(self, request, *args, **kwargs):
    #     print(request.data)
    #     doctor_obj = Doctors.objects.get(id=kwargs.get('pk'))
    #     print(doctor_obj.id, '++===++==+++==+++')
    #     logged_in_user = UserAuthentication.authenticate(self, request)[0]
    #     try:
    #         if logged_in_user.is_admin or logged_in_user.is_doctor:
    #             doctor_serializer = UpdateDoctorsSerializer(data=request.data)
    #             if doctor_serializer.is_valid():
    #                 try:
    #                     name = doctor_serializer.validated_data.get('name')
    #                     specialization = doctor_serializer.validated_data.get('specialization')
    #                     degree_name = doctor_serializer.validated_data.get('degree_name')
    #
    #                     experience = doctor_serializer.validated_data.get('experience')
    #                     email = doctor_serializer.validated_data.get('email')
    #                     mobile = doctor_serializer.validated_data.get('phone')
    #                     password = doctor_serializer.validated_data.get('password')
    #
    #                     doc_image = doctor_serializer.validated_data.get('profile_pic')
    #                     # password = make_password(password)
    #                     time_slots = doctor_serializer.validated_data.get('time_slots')
    #                     time_slots = ','.join(str(x) for x in time_slots)
    #
    #                     consultation_fee = doctor_serializer.validated_data.get('consultation_fee')
    #                     is_active = doctor_serializer.validated_data.get('is_active')
    #                     print(doctor_obj.user_id)
    #
    #                     user = Users.objects.filter(pk=doctor_obj.user_id).update(full_name=name, email=email,
    #                                                                               mobile=mobile, password=password,
    #                                                                               is_doctor=True)
    #                     print(user)
    #                     # print(user.mobile, user.full_name)
    #                     # UserDatabaseForNotification.objects.filter(phone_number=user.mobile).update(name=user.full_name,
    #                     #                                                                             phone_number=user.mobile,
    #                     #                                            email=user.email)
    #
    #                     doctor_obj = Doctors.objects.filter(pk=kwargs.get('pk')).update(name=name, specialization_id=specialization,
    #                                                                               degree_name=degree_name, experience=experience,
    #                                                                               time_slots=time_slots, consultation_fee=consultation_fee,
    #                                                                               is_active=is_active)
    #                     if doc_image:
    #                         try:
    #                             s3 = boto3.resource('s3', region_name='us-east-2',
    #                                                 aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
    #                                                 aws_secret_access_key='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')
    #                             s3.Bucket('detoxa').put_object(
    #                                 Key=doctor_serializer.validated_data.get('doc_image').name,
    #                                 Body=doctor_serializer.validated_data.get('doc_image'),
    #                                 ACL='public-read',
    #                                 ContentType=doctor_serializer.validated_data.get('doc_image').content_type,
    #                                 ContentDisposition='inline')
    #
    #                             doctor_obj.doc_image = f"https://detoxa.s3.us-east-2.amazonaws.com/{doc_image.name}"
    #                             doctor_obj.save()
    #                         except Exception as e:
    #                             print(e)
    #
    #                     doctor_obj_dict = {'id': doctor_obj.id}
    #                     doctor_obj_dict.update(doctor_serializer.data)
    #                     doctor_obj_dict.update({'doc_image': doctor_obj.doc_image})
    #
    #                     data = {
    #                         "success": True,
    #                         "message": "Doctor details updated successfully",
    #                         'doctor': doctor_obj_dict
    #                     }
    #                     return Response(data, status=status.HTTP_201_CREATED)
    #                 except Exception as e:
    #                     raise e
    #                 # return Response(doctor_serializer.data, status=status.HTTP_201_CREATED)
    #             return Response({"message": doctor_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    #         return Response({"message": "You are not authorized to create hospital user"}, status=status.HTTP_401_UNAUTHORIZED)

        # except Exception as e:
        #     print(e)
        #     return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class GetAllDoctorsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_by_name')
    specialization = django_filters.CharFilter(method='filter_by_specialization')
    experience = django_filters.CharFilter(method='filter_by_experience')

    class Meta:
        model = Doctors
        fields = []

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(name__icontains=value)

    def filter_by_specialization(self, queryset, name, value):
        return queryset.filter(specialization__name__icontains=value)

    def filter_by_experience(self, queryset, name, value):
        return queryset.filter(experience__iexact=value)


class GetAllDoctors(generics.ListAPIView):
    authentication_classes = []
    serializer_class = GetAllDoctorsSerializer
    pagination_class = StandardResultsSetPagination
    filterset_class = GetAllDoctorsFilter

    def get(self, request, *args, **kwargs):

        doctor_obj = Doctors.objects.filter(is_active=True).order_by("-id")
        doctor_obj = GetAllDoctorsFilter(request.GET, queryset=doctor_obj).qs.distinct()
        data_list = list()
        total_count = Doctors.objects.filter(is_active=True).count()
        for doctor in doctor_obj:
            data = GetAllDoctorsSerializer(doctor).data
            data['specialization'] = doctor.specialization.name
            data_list.append(data)
        reports = self.paginate_queryset(data_list)

        authorization_token = request.META.get('HTTP_AUTHORIZATION', None)
        if authorization_token:
            logged_in_user = UserAuthentication.authenticate(self, request)[0]

            fav_obj = Favourites.objects.filter(user=logged_in_user)
            fav_doct_serializer = FavouritesSerializer(fav_obj, many=True)
            return Response({'data': reports, 'count': total_count, 'favourites': fav_doct_serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({'data': reports, 'count': total_count},
                            status=status.HTTP_200_OK)

# class GetAllDoctors(generics.ListAPIView):
#     authentication_classes = []
#     serializer_class = GetAllDoctorsSerializer
#     filterset_class = GetAllDoctorsFilter
#     pagination_class = StandardResultsSetPagination
#
#     def get(self, request, *args, **kwargs):
#         doctor_obj = Doctors.objects.filter(is_active=True).order_by('-id')
#         page = self.paginate_queryset(doctor_obj)
#         data_list = GetAllDoctorsSerializer(page, many=True).data
#         print(data_list, '=========')
#         # doctor_obj = GetAllDoctorsFilter(request.GET, queryset=doctor_obj).qs.distinct()
#         # data_list = list()
#         # for doctors in doctor_obj:
#         #     data = GetAllDoctorsSerializer(doctors).data
#         #     data['specialization'] = doctors.specialization.name
#         #     data_list.append(data)
#         # data = []
#         # data.append(data_list)
#         # data.append({'count':len(doctor_obj)})
#         # data_list.append({'count': len(doctor_obj)})
#         return Response(data_list, status=status.HTTP_200_OK)


class CreateSpecialization(generics.CreateAPIView):
    authentication_classes = []
    parser_classes = (MultiPartParser,)
    serializer_class = SpecializationSerializer

    def post(self, request, *args, **kwargs):
        specialization_serializer = SpecializationSerializer(data=request.data)
        if specialization_serializer.is_valid():
            name = specialization_serializer.validated_data.get('name')
            image_url= None
            if specialization_serializer.validated_data.get('specialist_image'):
                try:
                    s3 = boto3.resource('s3', region_name='us-east-2',
                                        aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                                        aws_secret_access_key='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')
                    s3.Bucket('detoxa').put_object(Key=specialization_serializer.validated_data.get('specialist_image').name, Body=specialization_serializer.validated_data.get('specialist_image'), ACL='public-read',
                                                    ContentType=specialization_serializer.validated_data.get('specialist_image').content_type, ContentDisposition='inline')
                    image_url = f"https://detoxa.s3.us-east-2.amazonaws.com/{specialization_serializer.validated_data.get('specialist_image').name}"
                except Exception as e:
                    print(e)
            data = Specialization.objects.create(name=name,specialist_image=image_url)
            data_dict = {'id': data.id, 'name': data.name, 'specialist_image': data.specialist_image}
            return Response({"msg":"Specializtion created successfully",'data':data_dict}, status=status.HTTP_201_CREATED)
        else:
            return Response(specialization_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteSpecialization(generics.DestroyAPIView):
    authentication_classes = []

    def delete(self, request, *args, **kwargs):
        specialization_id = kwargs.get('pk')
        if Doctors.objects.filter(specialization__id=specialization_id).exists():
            return Response({"msg": "This Specilaization cannot be deleted. Specialization is associated with one or more doctors"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                specialization_obj = Specialization.objects.get(id=specialization_id)
                specialization_obj.delete()
                return Response({"msg":"Specialization deleted successfully"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"msg":"Specialization not found"}, status=status.HTTP_404_NOT_FOUND)


class GetAllSpecialization(generics.ListAPIView):
    authentication_classes = []
    serializer_class = GetAllSpecializationSerializer

    def get(self, request, *args, **kwargs):
        specialization_obj = Specialization.objects.filter(is_active=True)
        data_list = []
        for specialization in specialization_obj:
            data = GetAllSpecializationSerializer(specialization).data
            data_list.append(data)
        return Response(data_list, status=status.HTTP_200_OK)


class GetDoctorsById(generics.ListAPIView):
    authentication_classes = []
    serializer_class = GetAllDoctorsSerializer

    def get(self, request, *args, **kwargs):
        UserAuthentication.authenticate(self, request)[0]
        doc_obj = Doctors.objects.filter(id=kwargs['pk']).first()
        if doc_obj:
            data = GetAllDoctorsSerializer(doc_obj).data
            data['specialization_id'] = doc_obj.specialization.id
            data['specialization'] = doc_obj.specialization.name
            try:
                bank_details = BankDetails.objects.filter(user=doc_obj.user).first()
            except:
                bank_details = None
            data['bank_details'] = SaveBankDetailsSerializer(bank_details,many=False).data
            data = {
                "success": True,
                "data": data
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            raise exceptions.NotFound('Doctor not found')


class DeleteDoctors(generics.DestroyAPIView):
    authentication_classes = []
    serializer_class = GetAllDoctorsSerializer

    def delete(self, request, *args, **kwargs):
        UserAuthentication.authenticate(self, request)[0]
        doc_obj = Doctors.objects.filter(id=kwargs['pk']).first()
        if Appointment.objects.filter(doctor=doc_obj,status='Pending').exists():
            return Response({"msg": "This Doctor cannot be deleted. Doctor is associated with one or more appointments"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if doc_obj:
                # doc_obj.is_active = False
                # doc_obj.save()
                doc_obj.delete()
                data = {
                    "success": True,
                    "message": "Doctor deleted successfully"
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                raise exceptions.NotFound('Doctor not found')


class SaveBankDetails(generics.CreateAPIView):
    serializer_class = SaveBankDetailsSerializer
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        serializer = SaveBankDetailsSerializer(data=request.data)
        if serializer.is_valid():
            user_obj = None
            try:
                user_obj = Users.objects.get(id=serializer.validated_data.get('user_id'))
            except Exception as e:
                return Response({"message":str(e)},status=status.HTTP_400_BAD_REQUEST)
            bank_obj = None
            if user_obj.is_doctor:
                if BankDetails.objects.filter(account_number=serializer.validated_data.get('account_number')).exists():
                    return Response({'message':'This account number is already registerd'},status=status.HTTP_400_BAD_REQUEST)
                
                bank_obj = BankDetails.objects.create(
                    user=user_obj,
                    account_holder_name=serializer.validated_data.get('account_holder_name'),
                    account_number=serializer.validated_data.get('account_number'),
                    ifsc_code=serializer.validated_data.get('ifsc_code'),
                    bank_name=serializer.validated_data.get('bank_name'),
                    branch_name=serializer.validated_data.get('branch_name'),
                    account_type=serializer.validated_data.get('account_type'),
                    branch_address=serializer.validated_data.get('branch_address'),
                    is_doctor=True
                    )
            else:
                if BankDetails.objects.filter(account_number=serializer.validated_data.get('account_number')).exists():
                    return Response({'message':'This account number is already registerd'},status=status.HTTP_400_BAD_REQUEST)
                
                bank_obj = BankDetails.objects.create(
                    user=user_obj,
                    account_holder_name=serializer.validated_data.get('account_holder_name'),
                    account_number=serializer.validated_data.get('account_number'),
                    ifsc_code=serializer.validated_data.get('ifsc_code'),
                    bank_name=serializer.validated_data.get('bank_name'),
                    branch_name=serializer.validated_data.get('branch_name'),
                    account_type=serializer.validated_data.get('account_type'),
                    branch_address=serializer.validated_data.get('branch_address'),
                    is_therapist=True
                    )
                data = {'id':bank_obj.id}
                data.update(serializer.data)
            return Response({'data':data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateBankDetails(generics.UpdateAPIView):
    serializer_class = SaveBankDetailsSerializer
    parser_classes = (MultiPartParser,)

    def put(self,request,*args,**kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        serializer = SaveBankDetailsSerializer(data=request.data)
        if serializer.is_valid():
            try:
                bank_obj = BankDetails.objects.get(id=kwargs.get('pk'))
                bank_obj.account_holder_name = serializer.validated_data.get('account_holder_name')
                bank_obj.account_number = serializer.validated_data.get('account_number')
                bank_obj.ifsc_code = serializer.validated_data.get('ifsc_code')
                bank_obj.bank_name = serializer.validated_data.get('bank_name')
                bank_obj.branch_name = serializer.validated_data.get('branch_name')
                bank_obj.account_type = serializer.validated_data.get('account_type')
                bank_obj.branch_address = serializer.validated_data.get('branch_address')
                bank_obj.save()
                return Response({'msg':'Details update successfully','data':serializer.data}, status=status.HTTP_201_CREATED)
            except Exception as e:
                print(e)
                return Response({"message":str(e)},status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetDashBoardDetails(generics.ListAPIView):

    def get(self,request,*args,**kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        if logged_in_user.is_doctor:
            doctor_obj = Doctors.objects.get(user=logged_in_user)
            appointments = Appointment.objects.filter(doctor=doctor_obj)
            appointments_count = appointments.count()
            appointments_fees = appointments.aggregate(Sum('fees'))
            active_appointments = Appointment.objects.filter(doctor=doctor_obj).exclude(status='Completed').count()
            recent_appointments = Appointment.objects.filter(doctor=doctor_obj).order_by('-id')[:10]
            todays_appointments_count = Appointment.objects.filter(doctor=doctor_obj,date=datetime.date.today()).count()
            todays_appointments = Appointment.objects.filter(doctor=doctor_obj,date=datetime.date.today())
            todays_appointments_fees = todays_appointments.aggregate(Sum('fees'))
            return Response({"message":"Data fetched successfully",'total_appointents':appointments_count,"active_appointments":active_appointments,"appointment_fees":appointments_fees['fees__sum'],'recent_appointments':AppointmentSerailizer(recent_appointments,many=True).data,'todays_appointments_count':todays_appointments_count,'todays_appointments':AppointmentSerailizer(todays_appointments,many=True).data,'todays_appointments_fees':todays_appointments_fees},status=status.HTTP_400_BAD_REQUEST)
        elif logged_in_user.is_therapist:
            therapist_obj = therapist.Therapist.objects.get(user=logged_in_user)
            therapies = TherapySession.objects.filter(therapist=therapist_obj)
            appointments_count = therapies.count()
            active_appointments = TherapySession.objects.filter(therapist=therapist_obj).exclude(status='Completed').count()
            appointments_fees = therapies.aggregate(Sum('fees'))
            recent_appointments = TherapySession.objects.filter(therapist=therapist_obj).order_by('-id')[:10]
            todays_appointments_count = TherapySession.objects.filter(therapist=therapist_obj,date=datetime.date.today()).count()
            todays_appointments = TherapySession.objects.filter(therapist=therapist_obj,date=datetime.date.today())
            todays_appointments_fees = todays_appointments.aggregate(Sum('fees'))
            return Response({"message":"Data fetched successfully",'total_appointents':appointments_count,"active_appointments":active_appointments,"appointment_fees":appointments_fees['fees__sum'],'recent_appointments':TherapistAppointmentSerailizer(recent_appointments,many=True).data,'todays_appointments_count':todays_appointments_count,'todays_appointments':TherapistAppointmentSerailizer(todays_appointments,many=True).data,'todays_appointments_fees':todays_appointments_fees},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':'Invalid User'},status=status.HTTP_400_BAD_REQUEST)