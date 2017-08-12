from django.db import models
from accounts.models import Candidate
from postings.models import Posting

class Match(models.Model):
    """
    THis class describes the relationship between a candidate and a job posting they have been matched too
    it also contains information about the strength of the match
    """
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE
    )
    posting   = models.ForeignKey(
        Posting,
        on_delete=models.CASCADE
    )
    psycho_score = models.FloatField()
    psycho_type  = models.CharField(max_length=50)
    skill_score = models.FloatField()
    interest_score = models.FloatField()
    location_score = models.FloatField()
    total_match_score = models.FloatField()

    def __str__(self):
        return "{} - {}".format(self.candidate, self.posting)