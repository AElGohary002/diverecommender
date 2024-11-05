from django.db import models

class DiveDestination(models.Model):
    continent = models.CharField(max_length=500)
    country = models.CharField(max_length=500)
    link = models.URLField()
    dive_types = models.TextField()
    logged_species = models.IntegerField()
# Create your models here.

    def __str__(self):
        return f"{self.country} ({self.continent})"