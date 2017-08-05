from django.db import models

class Industry(models.Model):
    """
    Descriptive model of a type of industry
    """
    industry_choices = (
            ('AERO', 'Aerospace Industry'),
            ('AGRI', 'Agriculture'),
            ('CHEM', 'Chemical Industry'),
            ('COMP', 'Computer Industry'),
            ('CONS', 'Construction'),
            ('DEFE', 'Defense Industry'),
            ('EDUC', 'Education'),
            ('ENER', 'Energy Industry'),
            ('ENTE', 'Entertainment Industry'),
            ('FINA', 'Financial Services'),
            ('FOOD', 'Food Industry'),
            ('HEAL', 'Healthcare Industry'),
            ('HOSP', 'Hospitality Industry'),
            ('INFO', 'Infomation Industry'),
            ('MANU', 'Manufacturing Industry'),
            ('MASS', 'Mass Media'),
            ('TELE', 'Telecommunications Industry'),
            ('TRAN', 'Transport Industry'),
            ('WATE', 'Water Industry')
        )

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=industry_choices, blank=True)

    def __str__(self):
        return "{}".format(self.name)

class Interest(models.Model):

    name = models.CharField(max_length=100)
    category = models.TextField()

    def __str__(self):
        return "{}".format(self.name)

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


