from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)


class Pet(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    pet_name = models.CharField(max_length=50)
    pet_type = models.CharField(max_length=50)
    pet_species = models.CharField(max_length=200)

    def __str__(self):
        return self.pet_name


class Habitat(models.Model):
    inhabitant = models.ForeignKey(Pet, on_delete=models.CASCADE)
    actual_temperature = models.FloatField()
    actual_insolation = models.FloatField()
    habitat_type = models.CharField(max_length=150, default="")


class TemperatureLog(models.Model):
    source_habitat = models.ForeignKey(Habitat, on_delete=models.CASCADE)
    value = models.FloatField()


class InsolationLog(models.Model):
    source_habitat = models.ForeignKey(Habitat, on_delete=models.CASCADE)
    value = models.FloatField()


class ApiKey(models.Model):
    api_key = models.CharField(max_length=100, default="", unique=True)
    habitat_owner = models.ForeignKey(Habitat, on_delete=models.CASCADE)


