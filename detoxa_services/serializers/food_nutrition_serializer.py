from detoxa_services.models.food_nutrition_models import FoodNutrition
from rest_framework import serializers

from detoxa_services.models.users import Users

class FoodNutritionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    parent_user = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())
    child_user = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())
    gender = serializers.ChoiceField(choices=['Male','Female'])
    lunch = serializers.JSONField(help_text='this field require a  json object containing infromation about food name,amount,unit and calories for lunch e.g.{"food_1":{"description":"rice","amount":40,"unit":"gram","calories":120},"food_2":{"description":"rice","amount":40,"unit":"gram","calories":120}}')
    dinner = serializers.JSONField(help_text='this field require a  json object containing infromation about food name,amount,unit and calories for lunch e.g.{"food_1":{"description":"rice","amount":40,"unit":"gram","calories":120},"food_2":{"description":"rice","amount":40,"unit":"gram","calories":120}}')
    breakfast = serializers.JSONField(help_text='this field require a  json object containing infromation about food name,amount,unit and calories for lunch e.g.{"food_1":{"description":"rice","amount":40,"unit":"gram","calories":120},"food_2":{"description":"rice","amount":40,"unit":"gram","calories":120}}')
    current_height = serializers.CharField()
    current_weight = serializers.CharField()
    age = serializers.IntegerField()
    # class Meta:
        # model = FoodNutrition
        # fields = ['id','parent_user','child_user','gender','lunch','dinner','breakfast','current_height','current_weight','age']
        # depth = 4