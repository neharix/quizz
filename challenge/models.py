from django.db import models


class Question(models.Model):
    question = models.TextField()
    challenge = models.ForeignKey("Challenge", on_delete=models.CASCADE)
    point = models.IntegerField()

    def __str__(self):
        return self.question


class Challenge(models.Model):
    name = models.CharField(max_length=150, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_start = models.DateTimeField()
    date_finish = models.DateTimeField()
    is_public = models.BooleanField(default=False)

    # add time for challenge
    def __str__(self):
        return self.name


class Answer(models.Model):
    answer = models.TextField()
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    is_true = models.BooleanField(default=False)

    def __str__(self):
        return self.answer


class UserAnswer(models.Model):
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    answer = models.IntegerField()
    is_true = models.BooleanField(default=False)

    def __str__(self):
        return str(self.is_true)
