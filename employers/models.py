from django.db import models
from accounts.models import User
from commons.models.commons import Interest, Industry
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

    employed_by_company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.user.id
        super().save(*args, **kwargs)

    def __str__(self):
        if self.employed_by_company is not None:
            return "{} {} @ {}".format(self.user.first_name, self.user.last_name, self.employed_by_company.company_name)
        else:
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
    company_sizes = (
        ('0', '1-5'),
        ('1', '6-10'),
        ('2', '11-20'),
        ('3', '21-50'),
        ('4', '51-100'),
        ('5', '100+')
    )

    company_name = models.CharField(max_length=255)
    short_bio = models.CharField(max_length=140)
    long_bio = models.TextField()
    size = models.CharField(max_length=20, choices=company_sizes)

    #social media
    twitter  = models.URLField(blank = True)
    linkedin = models.URLField(blank = True)
    website  = models.URLField(blank = True)
    facebook = models.URLField(blank = True)

    company_lead = models.ForeignKey(
        'Employer',
        on_delete = models.CASCADE,
        blank = False
    )

    industries = models.ManyToManyField(
        Industry,
        through='CompanyIndustry',
        blank=True
    )

    def __str__(self):
        return "{}".format(self.company_name)

    class Meta:
        verbose_name_plural = 'Companies'

class CompanyIndustry(models.Model):
    """
    Controls the relationship between a company and an industry type
    """
    industry = models.ForeignKey(
        Industry,
        on_delete=models.PROTECT
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
    )


class Team(models.Model):
    """
    Group multiple people together within a team that belongs to a company
    """
    team_name = models.CharField(max_length=255)
    company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return "{}".format(self.team_name)
