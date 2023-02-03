from django.db import models

class RecommendedMeals(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    image_url = models.URLField(max_length=200, null=True)
    para_1 = models.TextField()
    para_2 = models.TextField()
    para_3 = models.TextField()
    para_4 = models.TextField()
    is_active = models.BooleanField(default=True)
