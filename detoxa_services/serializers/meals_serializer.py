from rest_framework import serializers
from detoxa_services.models.meals_models import RecommendedMeals


class RecommendedMealsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendedMeals
        fields = ['id', 'title', 'description', 'image_url', 'is_active','para_1','para_2','para_3','para_4']
        depth = 1
        read_only_fields = fields


class RecommendedMealsCreateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    image = serializers.ImageField(required=True)
    # is_active = serializers.BooleanField(required=False, default=True)
    para_1 = serializers.CharField(required=False)
    para_2 = serializers.CharField(required=False)
    para_3 = serializers.CharField(required=False)
    para_4 = serializers.CharField(required=False)




