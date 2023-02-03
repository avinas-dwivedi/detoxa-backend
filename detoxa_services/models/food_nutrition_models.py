from django.db import models
from .users import Users



class FoodNutrition(models.Model):
    parent_user = models.ForeignKey(Users,on_delete=models.CASCADE,related_name='food_nutrition_parent_user')
    child_user = models.ForeignKey(Users,on_delete=models.CASCADE)
    gender = models.CharField(max_length=200)
    lunch = models.JSONField()
    dinner = models.JSONField()
    breakfast = models.JSONField()
    current_height = models.CharField(max_length=200)
    current_weight = models.CharField(max_length=200)
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)