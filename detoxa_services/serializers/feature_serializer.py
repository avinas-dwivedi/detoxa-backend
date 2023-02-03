from pyexpat import features
from rest_framework import serializers
from detoxa_services.models.features import Feature

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'

class UpdateFeatureSerializer(serializers.Serializer):
    enable_features = serializers.ListField()
    disable_features = serializers.ListField()