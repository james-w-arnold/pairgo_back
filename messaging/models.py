from django.db import models
from accounts.models import User
from postings.models import Posting
from matching.models import Match

class Message(models.Model):
    """
    Describes a message that exists within a thread
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    time_sent = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=255)
    thread = models.ForeignKey(
        'Thread',
        on_delete=models.CASCADE
    )

class Thread(models.Model):
    """
    Object to describe a thread which links users together and allows for them to message
    """
    time_created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=30)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(
        User,
        through='ThreadUser'
    )

class ThreadUser(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE
    )