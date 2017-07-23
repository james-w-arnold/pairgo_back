from django.db import models


class Industry(models.Model):
    """
    Descriptive model of a type of industry
    """
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name

class Location(models.Model):
    """
    Descriptive model of a location
    """
    title = models.CharField(max_length=200)
    lat   = models.FloatField(verbose_name='latitude')
    lon   = models.FloatField(verbose_name='longitude')

    def __str__(self):
        return "{} - {}-{}".format(self.title, self.lat, self.lon)


class Skill(models.Model):
    """
    Descriptive model of a type of skill
    """
    name = models.TextField(unique=True)
    category = models.TextField()

    def __str__(self):
        return "{}".format(self.name)