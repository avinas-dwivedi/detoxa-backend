from rest_framework import serializers
from ..models.vaccination import *


class AddVaccinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccinationData
        fields = ['id', 'title', 'description', 'min_age', 'max_age']


class GetAllVaccineSerializer(serializers.ModelSerializer):

    class Meta:
        model = VaccinationData
        fields = ['id', 'title', 'description', 'min_age', 'max_age', 'is_active']


class VaccineStatusSerializer(serializers.ModelSerializer):
    vaccine_id = serializers.IntegerField()

    class Meta:
        model = MyVaccinationDetails
        fields = ['vaccine_id', 'status']


class SetReminderVaccineSerializer(serializers.Serializer):

    vaccine_id = serializers.IntegerField()
    reminder_date = serializers.CharField()
    reminder_time = serializers.CharField()

    class Meta:
        fields = ['vaccine_id', 'reminder_date', 'reminder_time']


class CancelVaccinationSerializer(serializers.Serializer):
    vaccine_id = serializers.IntegerField()

    class Meta:
        fields = ['vaccine_id']


class BookVaccinationAppointmentSerializer(serializers.Serializer):
    vaccine_id = serializers.IntegerField()
    child_id = serializers.IntegerField()
    appointment_date = serializers.DateField()
    appointment_time = serializers.TimeField()

    class Meta:
        fields = ['vaccine_id', 'child_id','appointment_date','appointment_time']