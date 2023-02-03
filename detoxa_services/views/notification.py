import base64

from rest_framework import generics
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from detoxa_services.models.notification_models import Notifications
from detoxa_services.serializers.notification_serializer import GetNotificationSerializer, MakemUserAdminSerializer, NotificationSerializer, ToSendNotificationsSerializer
from detoxa_services.tasks.send_notifications import send_notifications, send_notifications_excel
from detoxa_services.utils.user_authentication import UserAuthentication
from detoxa_services.views.organizations_views import StandardResultsSetPagination
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from ..models.users import Users


class NotificationListView(ListAPIView):
    serializer_class = GetNotificationSerializer
    pagination_class = StandardResultsSetPagination
    authentication_class = []

    notification_param = openapi.Parameter('notification_type', openapi.IN_QUERY, description="Notification type should be passed to get the list of notifications based on their type.",required=False, type=openapi.TYPE_STRING, enum=['Email', 'SMS', 'WhatsApp Notification'])
    from_date = openapi.Parameter('from_date', openapi.IN_QUERY,description='Enter a valid date in fromat YY-MM-DD',required=False, type=openapi.TYPE_STRING)
    to_date = openapi.Parameter('to_date', openapi.IN_QUERY,description='Enter a valid date in fromat YY-MM-DD',required=False, type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[notification_param,from_date,to_date])
    def get(self, request, *args, **kwargs):
        if request.query_params.get('from_date') and request.query_params.get('to_date') and request.query_params.get('notification_type'):
            notifications_type = request.query_params.get('notification_type')
            from_date = request.query_params.get('from_date')
            to_date = request.query_params.get('to_date')
            notifications = Notifications.objects.filter(from_date__lte=to_date, to_date__gte=from_date,notification_type=notifications_type,is_active=True)
            page = self.paginate_queryset(notifications)
            serializer = GetNotificationSerializer(page, many=True)
            return Response({"data":serializer.data,"count":Notifications.objects.filter(is_active=True).count(),"status":HTTP_200_OK})
        notifications = Notifications.objects.filter(is_active=True)
        page = self.paginate_queryset(notifications)
        serializer = GetNotificationSerializer(page, many=True)
        return Response({"data":serializer.data,"count":Notifications.objects.filter(is_active=True).count(), "status":HTTP_200_OK})


class CreateNotifications(CreateAPIView):
    queryset = Notifications.objects.all()
    serializer_class = NotificationSerializer
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        # logged_in_user = UserAuthentication.authenticate(self, request)[0]
        # if logged_in_user.is_super_admin:
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                Notifications.objects.create(**serializer.validated_data)
                return Response({"message": "Notification created successfully"}, status=HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        # else:
        #     return Response({'error': 'You are not authorized to perform this action'}, status=HTTP_400_BAD_REQUEST)


class UpdateNotifications(UpdateAPIView):
    model = Notifications
    serializer_class = NotificationSerializer

    def put(self, request, *args, **kwargs):
        UserAuthentication.authenticate(self, request)[0]
        try:
            notification_obj_exist = self.model.objects.filter(pk=kwargs.get('pk')).exists()
            if notification_obj_exist:
                notification_obj = self.model.objects.get(pk=kwargs.get('pk'))
                serializer = self.serializer_class(notification_obj, data=request.data)
                if serializer.is_valid():
                    notification_obj.notification_type = serializer.validated_data.get('notification_type')
                    notification_obj.title = serializer.validated_data.get('title')
                    notification_obj.message = serializer.validated_data.get('message')
                    notification_obj.from_date = serializer.validated_data.get('from_date')
                    notification_obj.to_date = serializer.validated_data.get('to_date')
                    notification_obj.is_active = serializer.validated_data.get('is_active')
                    notification_obj.save()
                    return Response({"success": True, "message": "Notification update successfully"}, status=HTTP_200_OK)
                else:
                    return Response({"success": False, "message": serializer.errors}, status=HTTP_400_BAD_REQUEST)
            return Response({"success": False, "message": "Notification ID Not Exist"}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=HTTP_400_BAD_REQUEST)


class DeleteNotifications(generics.DestroyAPIView):
    def delete(self, request, *args, **kwargs):
        try:
            UserAuthentication.authenticate(self, request)[0]
            notification_qs = Notifications.objects.filter(pk=kwargs.get('pk'))
            if len(notification_qs) > 0:
                notification_qs.delete()
                return Response({"success": True, "message": "Notification Delete successfully"}, status=HTTP_200_OK)
            else:
                return Response({"success": False, "message": "Notification ID Not Exist"}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"success": False, 'error': str(e)}, status=HTTP_400_BAD_REQUEST)


class NotificationGetView(ListAPIView):
    def get(self, request, *args, **kwargs):
        try:
            UserAuthentication.authenticate(self, request)[0]
            notification_qs = Notifications.objects.filter(pk=kwargs.get('pk'))
            if len(notification_qs) > 0:
                serializer = GetNotificationSerializer(notification_qs, many=True)
                return Response({"success": True, "data": serializer.data}, status=HTTP_200_OK)
            else:
                return Response({"success": False, "message": "Notification ID Not Exist"}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"success": False, 'error': str(e)}, status=HTTP_400_BAD_REQUEST)



    

class SendNotificationsForExistingUser(GenericAPIView):
    serializer_class = ToSendNotificationsSerializer
    
    user_type = openapi.Parameter('user_type', openapi.IN_QUERY, description="User Type type should be passed to send notifications based on their type.",required=False, type=openapi.TYPE_STRING, enum=['School Admin', 'Society Admin', 'Company Admin','Hospital Admin','School Users','Society Users','Company Users','Hospital Users','Doctors','Normal Users'])
    @swagger_auto_schema(manual_parameters=[user_type])
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = ToSendNotificationsSerializer(data=request.data)
        if serializer.is_valid():
            notification_id = serializer.validated_data.get('notification_id')
            user_type = request.query_params.get('user_type')
            send_notifications.delay(notification_id,user_type)
            return Response({'msg': 'Notifications are being sent'}, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)  


class SendNotificationsExcelSheet(GenericAPIView):
    serializer_class = ToSendNotificationsSerializer
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, *args, **kwargs):
        serializer = ToSendNotificationsSerializer(data=request.data)
        if serializer.is_valid():
            notification_id = serializer.validated_data.get('notification_id')
            # excel_sheet = serializer.validated_data.get('excel_sheet')
            raw_file = self.request.FILES['excel_sheet']
            if not raw_file.content_type in ['application/vnd.ms-excel',
                                            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                            'application/vnd.ms-excel.sheet.binary.macroenabled.12']:
                return Response({'message': 'Invalid File type', 'status': HTTP_200_OK}, status=HTTP_400_BAD_REQUEST)
            excel_raw_bytes = raw_file.read()
            excel_base64 = base64.b64encode(excel_raw_bytes).decode('utf-8')
            send_notifications_excel.delay(notification_id,excel_base64)
            return Response({'msg': 'Notifications are being sent'}, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)



class MakeUserAdminApiView(GenericAPIView):
    serializer_class = MakemUserAdminSerializer

    def post(self, request, *args, **kwargs):
        serializer = MakemUserAdminSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user_obj = Users.objects.get(id=serializer.validated_data.get('user_id'))
                user_obj.is_admin = True
                user_obj.save()
                return Response({'msge':'Admin created successfully'}, status=HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
