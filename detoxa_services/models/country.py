from django.db import models


class CountryStates(models.Model):
    state_name = models.CharField(max_length=300)
    state_code = models.CharField(max_length=100)
    state_capital = models.CharField(max_length=300)
    audio_1_url = models.CharField(max_length=500)
    audio_2_url = models.CharField(max_length=500, null=True, blank=True)
    audio_3_url = models.CharField(max_length=500,null = True, blank=True)

    def __str__(self):
        return self.state_name


class Animals(models.Model):
    animal_type = models.CharField(max_length=50)
    animal_name = models.CharField(max_length=300)
    audio_1_url = models.CharField(max_length=500, null=True, blank=True)
    audio_2_url = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.animal_name


class Country(models.Model):
    country_name = models.CharField(max_length=100)
    audio_1_url = models.CharField(max_length=500, null=True, blank=True)
    audio_2_url = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.country_name


class Vehicle(models.Model):
    vehicle_name = models.CharField(max_length=100)
    audio_1_url = models.CharField(max_length=500, null=True, blank=True)
    audio_2_url = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.vehicle_name


class SolorSystem(models.Model):
    solor_name = models.CharField(max_length=100)
    audio_1_url = models.CharField(max_length=500, null=True, blank=True)
    audio_2_url = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.solor_name


class Profession(models.Model):
    profession_name = models.CharField(max_length=100)
    audio_1_url = models.CharField(max_length=500, null=True, blank=True)
    audio_2_url = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.profession_name