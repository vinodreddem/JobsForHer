from django.db import models

# Create your models here.
class WeatherData(models.Model):
    zipcode = models.PositiveIntegerField()
    country = models.CharField (max_length = 50)
    state = models.CharField(max_length = 50)
    weather = models.TextField()
    max_temp = models.SmallIntegerField()
    min_temp = models.SmallIntegerField()
    unit_type = models.CharField(max_length = 1)
    