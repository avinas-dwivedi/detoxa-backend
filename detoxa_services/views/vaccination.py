from ..models import *
from ..serializers.vaccination_serializer import *
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import exceptions
from ..utils.user_authentication import UserAuthentication
import django_filters
from ..constants.datetime_formats import *
from datetime import datetime, timedelta


class AddVaccineData(generics.GenericAPIView):
    authentication_class = []
    serializer_class = AddVaccinationSerializer

    def post(self, request):
        user = UserAuthentication.authenticate(self, request)[0]
        vaccine_serializer = AddVaccinationSerializer(data=request.data)
        if vaccine_serializer.is_valid():
            try:
                title = vaccine_serializer.validated_data.get('title', )
                description = vaccine_serializer.validated_data.get('description', )
                min_age = vaccine_serializer.validated_data.get('min_age', )
                max_age = vaccine_serializer.validated_data.get('max_age', )
                vaccine_obj = VaccinationData.objects.create(title=title, description=description, min_age=min_age,
                                                             max_age=max_age)
                if vaccine_obj:
                    data = {
                        "success": True,
                        "data": {
                            'id': vaccine_obj.id,
                            "title": vaccine_obj.title,
                            "description": vaccine_obj.description,
                            "min_age": vaccine_obj.min_age,
                            "max_age": vaccine_obj.max_age,
                            "is_active": vaccine_obj.is_active,
                        }

                    }
                    return Response(data, status=status.HTTP_201_CREATED)
                else:
                    raise exceptions.ValidationError('Vaccine Not Created')
            except Exception as e:
                raise e
        else:
            return Response(vaccine_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetVaccineFilter(django_filters.FilterSet):
    min_age = django_filters.NumberFilter(method='filter_by_min_age')
    max_age = django_filters.NumberFilter(method='filter_by_max_age')

    class Meta:
        model = VaccinationData
        fields = []

    def filter_by_min_age(self, queryset, name, value):
        return queryset.filter(min_age=value)

    def filter_by_max_age(self, queryset, name, value):
        return queryset.filter(max_age=value)


class GetAllVaccineByAgeGroup(generics.ListAPIView):
    authentication_class = []
    serializer_class = GetAllVaccineSerializer
    filterset_class = GetVaccineFilter

    def get(self, request, *args, **kwargs):
        user = UserAuthentication.authenticate(self, request)[0]
        vaccine_obj = VaccinationData.objects
        vaccine_obj = GetVaccineFilter(request.GET, queryset=vaccine_obj).qs.distinct()
        data_list = list()
        vaccine_list = list()
        for obj in vaccine_obj:
            # json_data = {"over_due": 0}
            vaccine_json = {"id": obj.id, "title": obj.title, "description": obj.description,
                            "min_age": obj.min_age, "max_age": obj.max_age, "is_active": obj.is_active,
                            "is_mark_done": False, "is_reminder_added": False, "due_date": "1 July, 2021"}

            vaccine_list.append(vaccine_json)
        json_output = {"success": True, "over_due": 0, "upcoming": 0, "done": 0, 'data': vaccine_list}
        data_list.append(json_output)
        return Response(data_list, status=status.HTTP_200_OK)


class VaccineMarkDone(generics.GenericAPIView):
    authentication_class = []
    serializer_class = VaccineStatusSerializer

    def post(self, request):
        user = UserAuthentication.authenticate(self, request)[0]
        serializer = VaccineStatusSerializer(data=request.data)
        if serializer.is_valid():
            try:
                vaccine_id = serializer.validated_data.get('vaccine_id')
                vaccine_status = serializer.validated_data.get('status')
                try:
                    if not VaccinationData.objects.get(id=int(vaccine_id)).is_active:
                        raise exceptions.ValidationError('Vaccine cant be mark as done.')
                except VaccinationData.DoesNotExist:
                    raise exceptions.ValidationError('Invalid Vaccine ID')
                vaccine_obj = MyVaccinationDetails.objects.create(user=user, vaccine_id=int(vaccine_id),
                                                                  status=vaccine_status)
                if vaccine_obj:
                    data = {
                        "success": True,
                        "data": {
                            'id': vaccine_obj.id,
                            'vaccine_id': vaccine_id,
                            'status': vaccine_obj.status
                        }
                    }
                    return Response(data, status=status.HTTP_201_CREATED)
                else:
                    raise exceptions.ValidationError('Error occured while marking it done.')
            except Exception as e:
                raise e
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SetVaccineReminderView(generics.GenericAPIView):
    authentication_class = []
    serializer_class = SetReminderVaccineSerializer

    def post(self, request):
        user = UserAuthentication.authenticate(self, request)[0]
        serializer = SetReminderVaccineSerializer(data=request.data)
        if serializer.is_valid():
            try:
                vaccine_id = serializer.validated_data.get('vaccine_id')
                reminder_date = serializer.validated_data.get('reminder_date')
                reminder_time = serializer.validated_data.get('reminder_time')
                try:
                    if not VaccinationData.objects.get(id=int(vaccine_id)).is_active:
                        raise exceptions.ValidationError('Can not set reminder for this vaccine.')
                except VaccinationData.DoesNotExist:
                    raise exceptions.ValidationError('Invalid Vaccine ID')

                reminder_date = datetime.strptime(reminder_date, date_format)
                reminder_time = datetime.strptime(reminder_time, time_format)
                vaccine_obj = MyVaccinationDetails.objects.filter(user=user, vaccine_id=int(vaccine_id)).first()
                if vaccine_obj:
                    vaccine_obj.reminder_date = reminder_date
                    vaccine_obj.reminder_time = reminder_time
                    vaccine_obj.is_reminder_added = True
                    vaccine_obj.save()
                else:
                    vaccine_obj = MyVaccinationDetails.objects.create(user=user,
                                                                      vaccine_id=int(vaccine_id),
                                                                      reminder_date=reminder_date,
                                                                      reminder_time=reminder_time,
                                                                      is_reminder_added=True)
                if vaccine_obj:
                    data = {
                        "success": True,
                        "data": {
                            'id': vaccine_obj.id,
                            'vaccine_id': vaccine_id,
                            'is_reminder_added': True
                        }
                    }
                    return Response(data, status=status.HTTP_201_CREATED)
                else:
                    raise exceptions.ValidationError('Error occured while adding reminder.')
            except Exception as e:
                raise e
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CancelVaccinationAppointmentView(generics.GenericAPIView):
    

    def post(self,request,*args,**kwargs):
        user = UserAuthentication.authenticate(self, request)[0]
        try:
            vaccine_obj = VaccinationAppointment.objects.get(id=kwargs.get('pk'))
            vaccine_obj.status = "Cancelled"
            vaccine_obj.save()
            return Response({"success":True,"data":"Vaccination cancelled successfully"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success":False,"data":str(e)},status=status.HTTP_400_BAD_REQUEST)


class BookVaccinationAppointment(generics.CreateAPIView):
    serializer_class = BookVaccinationAppointmentSerializer

    def post(self,request,*args,**kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        serializer = BookVaccinationAppointmentSerializer(data=request.data)
        if serializer.is_valid():
            try:
                vaccine_id = serializer.validated_data.get('vaccine_id')
                child_id = serializer.validated_data.get('child_id')
                appointment_date = serializer.validated_data.get('appointment_date')
                appointment_time = serializer.validated_data.get('appointment_time')
                VaccinationAppointment.objects.create(user=logged_in_user,child=Users.object.get(id=child_id),vaccine_id=vaccine_id,appointment_date=appointment_date,appointment_time=appointment_time,status="Pending")               
                return Response({"success":True,"data":"Vaccination appointment booked successfully"},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"success":False,"data":str(e)},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)