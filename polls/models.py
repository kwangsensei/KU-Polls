import datetime
from django.db import models
from django.utils import timezone

# Create your models here.

class Question(models.Model):
    """
    Question class create Question model that has
    a question text, publication date and ending date.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    end_date = models.DateTimeField("ending date", null=True)
    def was_published_recently(self):
        """
        was_published_recently() returns True if wohse question was published recently (older than 1 day).
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    """
    Choice class create Choice model that has choice text and a vote tally. 
    Each Choice is associated with a Question.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self) -> str:
        return self.choice_text
