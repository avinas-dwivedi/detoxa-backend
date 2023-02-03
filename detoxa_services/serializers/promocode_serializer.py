from rest_framework import serializers
from ..models.promocode_models import  Promocode


class CreatePromoCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Promocode
        fields = '__all__'


class PromocodeSerializer(serializers.ModelSerializer):
    code = serializers.CharField()

    class Meta:
        model = Promocode
        fields = ('code',)


class PromocodeListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Promocode
        fields = '__all__'
        