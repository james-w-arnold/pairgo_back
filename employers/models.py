from django.db import models
from accounts.models import User
class Employee(models.Model):
    """
    This is the base employee model which describes anyone affiliated with a company
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    about = models.TextField()
    job_title = models.CharField(max_length=255)

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)

class EmployerLead(models.Model):
    """
    This model describes the individual that is responsible for a specific company within the platform,
    they also have juristication over the employee individuals
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    about = models.TextField()
    job_title = models.CharField(max_length=255)

class Company(models.Model)