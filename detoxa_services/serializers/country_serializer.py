from rest_framework import serializers
from detoxa_services.models.country import CountryStates, Animals, Country, Vehicle, SolorSystem, Profession


class GetCountryStatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryStates
        fields = '__all__'


class GetAnimalsbyIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animals
        fields = '__all__'


class GetVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'


class GetSolarSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolorSystem
        fields = '__all__'


class GetProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = '__all__'


class GetCountryIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class GetStatesSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    audio_file = serializers.FileField(required=True)