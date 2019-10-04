from django.db import models

# Create your models here.
class Device(models.Model):
    device_name = models.CharField(max_length=100)

    def __str__(self):
        return f"DEVICE_NAME: {self.device_name}"