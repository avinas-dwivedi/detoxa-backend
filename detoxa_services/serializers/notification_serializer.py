from detoxa_services.models.notification_models import *
from rest_framework import serializers


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = '__all__'

class GetNotificationSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    notification_type = serializers.CharField(max_length=255,required=False)
    title = serializers.CharField(max_length=255,required=False)
    message = serializers.CharField(required=False)
    from_date = serializers.DateField(required=False)
    to_date = serializers.DateField(required=False)
    is_active = serializers.BooleanField(required=False)


class ToSendNotificationsSerializer(serializers.Serializer):
    notification_id = serializers.IntegerField()
    excel_sheet = serializers.FileField(required=False)
    # user_type = serializers.CharField(required=False)

class MakemUserAdminSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
