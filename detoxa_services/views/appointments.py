from asyncio.log import logger
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from detoxa_backend import settings

from detoxa_services.utils.user_authentication import UserAuthentication
from detoxa_services.views.organizations_views import StandardResultsSetPagination
from ..models.doctors import Doctors
from ..serializers.appointment_serializer import AppointmentSerializer, CreateAppointmentSerializer, UpdateAppointmentSerializer
from ..models.appointments_models import Appointment
from django.core.mail import send_mail

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from detoxa_services.models import appointments_models



class GetAllAppointments(ListAPIView):
    """
    Get all appointments for the logged in user
    """
    model = Appointment
    serializer_class = AppointmentSerializer
    pagination_class = StandardResultsSetPagination
    appointment_status_param = openapi.Parameter('status', openapi.IN_QUERY, required=False, type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[appointment_status_param])
    def get(self, request):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        appointment_status = request.GET.get('status')
        if appointment_status:
            if logged_in_user.is_doctor:
                doctor = Doctors.objects.filter(user=logged_in_user)
                appointments = Appointment.objects.filter(doctor=doctor[0].id,status=appointment_status).order_by('-date')
            else:
                appointments = Appointment.objects.filter(user=logged_in_user,status=appointment_status).order_by('-date')

            page = self.paginate_queryset(appointments)
            serializer = AppointmentSerializer(page, many=True)
            return Response({'data': serializer.data, 'count': Appointment.objects.all().count()})
        if logged_in_user.is_doctor:
            doctor = Doctors.objects.filter(user=logged_in_user)
            appointments = Appointment.objects.filter(doctor=doctor[0].id).order_by('-date')
        else:
            appointments = Appointment.objects.filter(user=logged_in_user).order_by('-date')
        page = self.paginate_queryset(appointments)
        serializer = AppointmentSerializer(page, many=True)
        return Response({'data': serializer.data, 'count': Appointment.objects.all().count()})
        

class CreateNewAppointment(CreateAPIView):
    """
    Create a new appointment for the logged in user
    """
    model = Appointment
    serializer_class = CreateAppointmentSerializer

    def post(self, request):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        serializer = CreateAppointmentSerializer(data=request.data)
        if serializer.is_valid():
            apponitement_obj = Appointment.objects.create(
                user=logged_in_user,
                doctor=serializer.validated_data['doctor'],
                child=serializer.validated_data['child'],
                description=serializer.validated_data['description'],
                date=serializer.validated_data['date'],
                slot=serializer.validated_data['slot'],
                fees=serializer.validated_data['fees'],
                is_promocode_applied=serializer.validated_data.get('is_promocode_applied'),
                promocode=serializer.validated_data.get('promocode'),
            )
            send_mail(f'Email for new Appointment ', f'Appointment has been booked successfully for {apponitement_obj.date} between {apponitement_obj.slot}', settings.FROM_EMAIL, [
                        logged_in_user.email], fail_silently=False)
            apponitement_obj_dict = {'id':apponitement_obj.id}
            apponitement_obj_dict.update(serializer.data)
            logger.info('appointment created successfully')
            return Response(apponitement_obj_dict, status=status.HTTP_201_CREATED)
        logger.error('appointment creation failed')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateAppointment(UpdateAPIView):
    """
    Update the status of an appointment
    """
    serializer_class = UpdateAppointmentSerializer

    def put(self, request, *args, **kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        try:
            appointment_obj = Appointment.objects.get(id=kwargs['pk'])
            if logged_in_user.is_doctor and appointment_obj.doctor.user == logged_in_user:
                serializer = UpdateAppointmentSerializer(appointment_obj, data=request.data)
                if serializer.is_valid():
                    appointment_obj.status = serializer.validated_data.get('status')
                    appointment_obj.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
            if appointment_obj.user == logged_in_user:
                appointment_obj.status = 'Cancelled'
                appointment_obj.save()
                send_mail(f'Email for Appointment Cancellation', f'Appointment for {appointment_obj.date} between {appointment_obj.slot} has been cancelled by you.', settings.FROM_EMAIL, [
                logged_in_user.email], fail_silently=False)

                logger.error('appointment not updated')
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            logger.info('appointment updated successfully')
            return Response({'message':'You are not authorized to perform this action','status':status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED)
        except Appointment.DoesNotExist:
            logger.error('appointment does not exist')
            return Response({'message':f'Appointment with id {kwargs["pk"]} does not exist','status':status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

# class CancelAppointment(GenericAPIView):
#     """
#     Cancel an appointment
#     """
#     serializer_class = UpdateAppointmentSerializer

#     def post(self, request, *args, **kwargs):
#         logged_in_user = UserAuthentication.authenticate(self, request)[0]
#         try:
#             appointment_obj = Appointment.objects.get(id=kwargs['pk'])
#             if appointment_obj.user == logged_in_user:
#                 appointment_obj.status = 'Cancelled'
#                 appointment_obj.save()
#                 return Response({'message':'Appointment cancelled successfully'}, status=status.HTTP_200_OK)
#             return Response({'message':'You are not authorized to perform this action','status':status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED)
#         except Appointment.DoesNotExist:
#             return Response({'message':f'Appointment with id {kwargs["pk"]} does not exist','status':status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)