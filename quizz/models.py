from django.db import models


class Challenge(models.Model):
    name = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    name = models.CharField(max_length=100)
    question = models.TextField()
    challenge = models.ForeignKey("Challenge", on_delete=models.PROTECT)
    point = models.IntegerField()

    def __str__(self):
        return self.name


class Answer(models.Model):
    answer = models.TextField()
    question = models.ForeignKey("Question", on_delete=models.PROTECT)
    is_true = models.BooleanField(default=False)

    def __str__(self):
        return self.answer


class UserAnswer(models.Model):
    question = models.IntegerField()
    answer = models.IntegerField()
    is_true = models.BooleanField(default=False)

    def __str__(self):
        return str(self.is_true)
