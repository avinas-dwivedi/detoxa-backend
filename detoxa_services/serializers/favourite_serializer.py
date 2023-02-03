from rest_framework import serializers
from detoxa_services.models.favourites import Favourites


class CreateFavouritesSerializer(serializers.Serializer):
    doctor = serializers.IntegerField(required=False)
    therapist = serializers.IntegerField(required=False)
    # class Meta:
    #     model = Favourites
    #     fields = ['doctor']


class FavouritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourites
        fields = '__all__'
        depth = 1