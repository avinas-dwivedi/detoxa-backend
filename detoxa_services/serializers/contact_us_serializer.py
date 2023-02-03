from ..models.contact_us import ContactUs
from rest_framework import serializers
from django.core.validators import EmailValidator


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ['full_name', 'email', 'mobile', 'message']
        extra_kwargs = {
                        'full_name': {'required': True}, 'email': {'required': True, 'validators': [EmailValidator]},
                        'mobile': {'required': True}, 'message': {'required': True}
                        }