from rest_framework import serializers
from detoxa_services.models.users import Users

class AddAddressSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False,read_only=True)
    # user = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())
    street = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    country = serializers.CharField()
    pincode = serializers.CharField()
