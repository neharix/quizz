from django.contrib.auth.models import User
from django.db import models


class Question(models.Model):
    question = models.TextField(null=True, blank=True)
    is_image = models.BooleanField(default=False)
    image = models.ImageField(upload_to="questions/", null=True, blank=True)
    challenge = models.ForeignKey("Challenge", on_delete=models.CASCADE)
    point = models.IntegerField()

    def __str__(self):
        return self.question


class Challenge(models.Model):
    name = models.CharField(max_length=150, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_start = models.DateTimeField()
    date_finish = models.DateTimeField()
    time_for_event = models.IntegerField(default=30)
    is_public = models.BooleanField(default=False)

    # add time for challenge
    def __str__(self):
        return self.name


class Answer(models.Model):
    answer = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="answers/", blank=True, null=True)
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    is_image = models.BooleanField(default=False)
    is_true = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk) + ". " + self.answer


class UserAnswer(models.Model):
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    answer = models.ForeignKey("Answer", on_delete=models.CASCADE)
    is_true = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.is_true)
