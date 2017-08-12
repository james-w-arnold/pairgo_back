from django.db import models
from employers.models import Company, Employer, Team, Employee
from commons.models.commons import *

class Posting(models.Model):
    """
    This is the class which is used to describe an internship posting for a specific company which can be matched
    to a student
    """
    role_types = (
        ('F', 'Full Time'),
        ('P', 'Part Time')
    )

    status_types = (
        ('0', 'Created'),
        ('1', 'Matches Found'),
        ('2', 'In Conversations'),
        ('3', 'Matched')
    )

    job_title = models.CharField(max_length = 100)
    role_type = models.CharField(max_length=20, choices=role_types)
    about = models.TextField()
    working_hours = models.FloatField()
    start_date = models.DateField()
    end_date   = models.DateField()
    description = models.TextField(blank=True)
    created_date = models.DateField(auto_now_add=True)
    closed_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=status_types)
    salary = models.FloatField(blank=True)
    #foreign keys
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
    )

    employer = models.ForeignKey(
        Employer,
        on_delete=models.CASCADE
    )

    interests = models.ManyToManyField(
        Interest,
        through='PostingInterest',
        blank=True
    )

    skills = models.ManyToManyField(
        Skill,
        through='PostingSkill',
        blank=True
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.DO_NOTHING,
        blank=True
    )

    employees = models.ManyToManyField(
        Employee,
        through='PostingEmployee',
        blank=True
    )

    locations = models.ManyToManyField(
        Location,
        through='PostingLocation',
        blank=True
    )

class PostingInterest(models.Model):
    """
    Through class to link a post to different interests
    """
    posting = models.ForeignKey(
        Posting,
        on_delete=models.CASCADE
    )
    interest = models.ForeignKey(
        Interest,
        on_delete=models.PROTECT
    )

class PostingSkill(models.Model):
    """
    Through class to link a post to different skills
    """
    posting = models.ForeignKey(
        Posting,
        on_delete=models.CASCADE
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.PROTECT
    )

class PostingEmployee(models.Model):
    """
    Through class to link many postings to many employees
    """
    posting = models.ForeignKey(
        Posting,
        on_delete=models.CASCADE
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT
    )

class PostingLocation(models.Model):
    """
    Through class to link postings to different locations
    """
    posting = models.ForeignKey(
        Posting,
        on_delete=models.CASCADE
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT
    )

class PostingPsychometrics(models.Model):
    """
    Model to describe the psychometric analysis of a post
    """
    posting = models.ForeignKey('Posting', on_delete=models.CASCADE)
    extroversion = models.IntegerField()
    neuroticism = models.IntegerField()
    openness_to_experience = models.IntegerField()
    conscientiousness = models.IntegerField()
    agreeableness = models.IntegerField()
