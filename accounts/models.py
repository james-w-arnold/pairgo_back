from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
import random
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
from commons.models import commons

# Create your models here.


class CustomUserManager(BaseUserManager):
    """
    Override the BassUserManager, allowing for us to produce a User models that is setup to meet the base needs of our
    platform
    """
    def create_user(self, email, first_name, last_name, password=None, **kwargs):
        """
        Creates and saves a User with the given email and password
        :return: a validated User object
        """

        if not email:
            raise ValueError('Users must have an email address')

        user = User(
            email=CustomUserManager.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name, last_name):
        user = self.create_user(email, password=password, first_name=first_name, last_name=last_name)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

def generate_id():
    """
    :return: A random ID to be used for the Primary key
    """
    return random.getrandbits(53)

class User(AbstractUser):
    """
    Custom user model for PairGo
    """
    id = models.BigIntegerField(primary_key=True,
                                default=generate_id,
                                editable=False)
    modified = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=150,
                                unique=True,
                                null=True)
    email = models.EmailField(unique=True,
                              verbose_name='email address',
                              max_length=255)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

class UserType(models.Model):
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE
    )
    isCandidate = models.BooleanField(default=False)
    isEmployer  = models.BooleanField(default=False)

class Candidate(models.Model):
    """
    Model to describe a student candidate within the system
    """
    id = models.BigIntegerField(primary_key=True,
                                default=generate_id(),
                                editable=False)
    about = models.TextField(blank=True)
    birth_date = models.DateField(null=True)
    right_to_work = models.NullBooleanField()
    linkedin_url = models.URLField(blank=True)

    locations = models.ManyToManyField(
        commons.Location,
        through='CandidateLocation',
        blank=True
    )
    skills = models.ManyToManyField(
        commons.Skill,
        through='CandidateSkill',
        blank=True
    )

    interests = models.ManyToManyField(
        commons.Interest,
        through='CandidateInterest',
        blank=True
    )

    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)

class CandidateEducation(models.Model):
    """
    Describes education
    """
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=100)
    level = models.CharField(max_length=20)
    grade = models.CharField(max_length=20)
    completed = models.BooleanField(default=False)

    user = models.ForeignKey(
        'Candidate',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return "{}-{}".format(self.institution, self.degree)

class CandidateLocation(models.Model):
    """
    Describe the relation between Users and models, multiple users can have multiple locations and visa versa
    """
    candidate = models.ForeignKey(
        'Candidate',
        on_delete=models.CASCADE
    )
    location = models.ForeignKey(
        commons.Location,
        on_delete=models.PROTECT
    )
    current = models.BooleanField()

class CandidateSkill(models.Model):
    """
    Describe the many to many relationship between candidates and skills
    """
    candidate = models.ForeignKey(
        'Candidate',
        on_delete=models.CASCADE
    )
    skill = models.ForeignKey(
        commons.Skill,
        on_delete=models.PROTECT
    )

class CandidateInterest(models.Model):

    candidate = models.ForeignKey(
        'Candidate',
        on_delete=models.CASCADE
    )
    interest = models.ForeignKey(
        commons.Interest,
        on_delete=models.PROTECT
    )

class CandidatePsychometrics(models.Model):
    """
    Hold information about the primary psychometric analysis
    """
    extroversion = models.IntegerField()
    neuroticism  = models.IntegerField()
    openness_to_experience = models.IntegerField()
    conscientiousness = models.IntegerField()
    agreeableness = models.IntegerField()

    user = models.ForeignKey(
        'Candidate',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return "{}".format(self.user)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)