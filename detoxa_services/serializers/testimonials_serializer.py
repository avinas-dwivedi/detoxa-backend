from rest_framework import serializers
from ..models.testimonials import Services, Testimonials
from ..constants import constants
from rest_framework import exceptions


class AddServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ['name']
        extra_kwargs = {'name': {'required': True}}


class GetAllServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ['id', 'name']


class RemoveServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ['id']


class AddTestimonialSerializer(serializers.ModelSerializer):
    picture_url = serializers.ImageField()

    class Meta:
        model = Testimonials
        fields = ['customer_name', 'service', 'picture_url', 'testimonial']
        extra_kwargs = {
            'customer_name': {'required': True},
            'service': {'required': True},
            'testimonial': {'required': True},
            'picture_url': {'required': True}
            }


class GetAllTestimonialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonials
        fields = ['id', 'customer_name', 'service', 'testimonial', 'picture_url', 'is_active']
        depth = 1


class GetTestimonialsByIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonials
        fields = ['id', 'customer_name', 'service', 'testimonial', 'picture_url', 'is_active']


class RemoveTestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonials
        fields = ['id']



