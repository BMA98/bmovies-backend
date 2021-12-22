from django.db import models


class Country(models.Model):
    """
    Defines a model for countries
    country_iso: the iso code of the country
    country_name: the name of the country
    """
    iso = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name
