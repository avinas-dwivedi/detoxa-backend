from rest_framework import serializers
from ..models.therapy_session import TherapySession


class TherapySessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TherapySession
        fields = '__all__'
        depth = 5


class CreateTherapySessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TherapySession
        fields = ['therapist', 'child', 'description', 'date', 'slot',
                  'fees', 'is_promo_code_applied', 'promo_code']

        extra_kwargs = {
            'is_promo_code_applied': {'required': False}, 'promo_code': {'required': False}
        }


class UpdateTherapySessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TherapySession
        fields = ['status']
        extra_kwargs = {
            'status': {'required': True}
        }

