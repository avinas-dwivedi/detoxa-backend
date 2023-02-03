import json as js
from django.db.models.fields import json
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.parsers import MultiPartParser, FormParser
from detoxa_services.utils.user_authentication import UserAuthentication
from detoxa_services.models.food_nutrition_models import FoodNutrition
from detoxa_services.serializers.food_nutrition_serializer import FoodNutritionSerializer
from django.utils.safestring import SafeString


class FoodNutritionAPIView(CreateAPIView):
    authentication_classes = []
    serializer_class = FoodNutritionSerializer
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        if logged_in_user:
            serializer = FoodNutritionSerializer(data=request.data)
            if serializer.is_valid():
                FoodNutrition.objects.create(
                    parent_user=logged_in_user,
                    child_user=serializer.validated_data['child_user'],
                    gender = serializer.validated_data['gender'],
                    lunch = serializer.validated_data['lunch'],
                    dinner = serializer.validated_data['dinner'],
                    breakfast = serializer.validated_data['breakfast'],
                    current_height=serializer.validated_data['current_height'],
                    current_weight=serializer.validated_data['current_weight'],
                    age=serializer.validated_data['age']
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)