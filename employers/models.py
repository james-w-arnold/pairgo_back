from django.db import models
from accounts.models import User
from commons.models.commons import Interest
class Employer(models.Model):
    """
    This is the base employee model which describes anyone affiliated with a company
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    about = models.TextField()
    job_title = models.CharField(max_length=255)
    is_lead = models.BooleanField(default=False)
    #psychometrics tied to them
    #team
    team = models.ForeignKey(
        'Team',
        on_delete=models.PROTECT,
        blank=True
    )
    interests = models.ManyToManyField(
        Interest,
        through='EmployerInterest',
        blank=True
    )

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)


class EmployerInterest(models.Model):
    employer = models.ForeignKey(
        Employer,
        on_delete=models.DO_NOTHING
    )
    interest = models.ForeignKey(
        Interest,
        on_delete=models.CASCADE
    )

class EmployerPsychometrics(models.Model):
    employer = models.ForeignKey(
        Employer,
        on_delete=models.CASCADE
    )
    extroversion = models.IntegerField()
    neuroticism  = models.IntegerField()
    openness_to_experience = models.IntegerField()
    conscientiousness = models.IntegerField()
    agreeableness = models.IntegerField()

    def __str__(self):
        return "{}".format(self.employer)

class Company(models.Model):
    """
    Description of a company
    """
    company_name = models.CharField(max_length=255)
    short_bio = models.CharField(max_length=140)
    long_bio = models.TextField()