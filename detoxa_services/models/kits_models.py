from django.db import models
from rest_framework import status

class KitCategory(models.Model):
    """
    Model for kit categories
    """
    name = models.CharField(max_length=50)
    image = models.URLField(max_length=2000, blank=True)

    def __str__(self):
        return self.name


class Kit(models.Model):
    """
    Model for kits
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(KitCategory, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    image_1 = models.URLField(blank=True)
    image_2 = models.URLField(blank=True)
    image_3 = models.URLField(blank=True)
    image_4 = models.URLField(blank=True)

    # def __str__(self):
    #     return str(self.id) + " - " + self.name


class KitImages(models.Model):
    kit = models.ForeignKey(Kit, on_delete=models.CASCADE)
    image = models.URLField(max_length=2000, blank=True)