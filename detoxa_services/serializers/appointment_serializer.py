from rest_framework import serializers
from ..models.appointments_models import  Appointment



class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        depth = 5

class CreateAppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = ['doctor','child','description','date','slot','fees','is_promocode_applied','promocode']
        extra_kwargs = {
                        'is_promocode_applied': {'required': False}, 'promocode':{'required':False}
                        }

class UpdateAppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = ['status']
        extra_kwargs = {
            'status': {'required': True}
        }
        
    