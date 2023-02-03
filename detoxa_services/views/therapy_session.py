from asyncio.log import logger
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from detoxa_backend import settings
from detoxa_services.utils.user_authentication import UserAuthentication
from detoxa_services.views.organizations_views import StandardResultsSetPagination
from ..serializers.therapy_session_serializer import TherapySessionSerializer, CreateTherapySessionSerializer, UpdateTherapySessionSerializer

from ..models.therapist import Therapist
from ..models.therapy_session import TherapySession
from django.core.mail import send_mail
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class GetAllTherapySession(ListAPIView):
    """
    Get all therapy session
    """
    model = TherapySession
    serializer_class = TherapySessionSerializer
    pagination_class = StandardResultsSetPagination

    therapy_status_param = openapi.Parameter('status', openapi.IN_QUERY, required=False, type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[therapy_status_param])
    def get(self, request):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        therapy_status = request.GET.get('status')
        if therapy_status:
            if logged_in_user.is_therapist:
                therapist = Therapist.objects.filter(user=logged_in_user)
                therapist_session = TherapySession.objects.filter(therapist=therapist[0].id, status=therapy_status).order_by('-date')
            else:
                therapist_session = TherapySession.objects.filter(user=logged_in_user, status=therapy_status).order_by('-date')

            page = self.paginate_queryset(therapist_session)
            serializer = TherapySessionSerializer(page, many=True)
            return Response({'data': serializer.data, 'count': TherapySession.objects.all().exclude(status='Cancelled').count()})
        if logged_in_user.is_therapist:
            therapist = Therapist.objects.filter(user=logged_in_user)
            therapist_session = TherapySession.objects.filter(therapist=therapist[0].id).order_by('-date')
        else:
            therapist_session = TherapySession.objects.filter(user=logged_in_user).order_by('-date')
        page = self.paginate_queryset(therapist_session)
        serializer = TherapySessionSerializer(page, many=True)
        return Response({'data': serializer.data, 'count': TherapySession.objects.all().exclude(status='Cancelled').count()})


class CreateNewTherapySession(CreateAPIView):
    """
    Create a new therapy session
    """
    model = TherapySession
    serializer_class = CreateTherapySessionSerializer

    def post(self, request):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        serializer = CreateTherapySessionSerializer(data=request.data)
        if serializer.is_valid():
            therapy_session_obj = TherapySession.objects.create(user=logged_in_user, therapist=serializer.validated_data['therapist'],
                                                                child=serializer.validated_data['child'],
                                                                description=serializer.validated_data['description'],
                                                                date=serializer.validated_data['date'],
                                                                slot=serializer.validated_data['slot'],
                                                                fees=serializer.validated_data['fees'],
                                                                is_promo_code_applied=serializer.validated_data.get('is_promo_code_applied'),
                                                                promo_code=serializer.validated_data.get('promo_code'),)
            send_mail(f'Email for new Therapy session ',
                      f'Therapy session has been booked successfully for {therapy_session_obj.date} between {therapy_session_obj.slot}',
                      settings.FROM_EMAIL, [
                          logged_in_user.email], fail_silently=False)
            therapy_session_obj_dict = {'id': therapy_session_obj.id}
            therapy_session_obj_dict.update(serializer.data)
            logger.info('Therapy session created successfully')
            return Response(therapy_session_obj_dict, status=status.HTTP_201_CREATED)
        logger.error('Therapy session creation failed')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateTherapySession(UpdateAPIView):
    """
    Update the status of a therapy session
    """
    serializer_class = UpdateTherapySessionSerializer

    def put(self, request, *args, **kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        try:
            therapy_session_obj = TherapySession.objects.get(id=kwargs['pk'])
            if logged_in_user.is_doctor or logged_in_user.is_therapist:
                serializer = UpdateTherapySessionSerializer(therapy_session_obj, data=request.data)
                if serializer.is_valid():
                    therapy_session_obj.status = serializer.validated_data.get('status')
                    therapy_session_obj.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
            if therapy_session_obj.user == logged_in_user:
                therapy_session_obj.status = 'Cancelled'
                therapy_session_obj.save()
                send_mail(f'Email for Therapy session Cancellation',
                          f'Therapy session for {therapy_session_obj.date} between {therapy_session_obj.slot} has been cancelled by you.',
                          settings.FROM_EMAIL, [logged_in_user.email], fail_silently=False)

                logger.error('Therapy session not updated')
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            logger.info('Therapy session updated successfully')
            return Response(
                {'message': 'You are not authorized to perform this action', 'status': status.HTTP_401_UNAUTHORIZED},
                status=status.HTTP_401_UNAUTHORIZED)
        except TherapySession.DoesNotExist:
            logger.error('therapy session does not exist')
            return Response({'message': f'Therapy session with id {kwargs["pk"]} does not exist', 'status': status.HTTP_404_NOT_FOUND},
                            status=status.HTTP_404_NOT_FOUND)
