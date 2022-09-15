import datetime
from django.db import models
from django.utils import timezone

# Create your models here.

class Question(models.Model):
    """
    Question class create a Question model that has
    a question text, publication date and ending date.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    end_date = models.DateTimeField("date ending", null=True)
    def was_published_recently(self):
        """
        was_published_recently() returns True if wohse question was published recently (older than 1 day).
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """
        is_published() returns True if current date is on or after question's publication date.
        """
        now = timezone.now()
        return now >= self.pub_date
        
    def can_vote(self):
        """
        can_vote() returns True if voting is allowed for this question.
        """
        now = timezone.now()
        if self.end_date:
            return self.pub_date <= now <= self.end_date
        return self.is_published()

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    """
    Choice class create a Choice model that has choice text and a vote tally. 
    Each Choice is associated with a Question.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self) -> str:
        return self.choice_text
