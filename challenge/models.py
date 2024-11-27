from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    about = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.user.username + "'s profile"


class Question(models.Model):
    question = models.TextField(null=True, blank=True)
    is_image = models.BooleanField(default=False)
    image = models.ImageField(upload_to="questions/", null=True, blank=True)
    challenge = models.ForeignKey("Challenge", on_delete=models.CASCADE)
    point = models.IntegerField(default=1)
    complexity = models.ForeignKey("Complexity", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.pk}. {self.question}"


class Challenge(models.Model):
    name = models.CharField(max_length=150, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_start = models.DateTimeField()
    date_finish = models.DateTimeField()
    time_for_event = models.IntegerField(default=30)
    is_public = models.BooleanField(default=False)
    questions_count = models.IntegerField()
    with_confirmation = models.BooleanField()
    image = models.ImageField(upload_to="challenge_covers/", blank=True, null=True)

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
        return f"{self.pk}. {self.answer}"


class UserAnswer(models.Model):
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    challenge = models.ForeignKey("Challenge", on_delete=models.CASCADE)
    answer = models.ForeignKey("Answer", on_delete=models.CASCADE, null=True)
    is_true = models.BooleanField(default=False)
    is_empty = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answered_at = models.DateTimeField()

    def __str__(self):
        return str(self.is_true)


class TestSession(models.Model):
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    questions_json = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.user.username} {self.challenge.name}"


class Complexity(models.Model):
    level = models.CharField(max_length=100)

    def __str__(self):
        return self.level


class ConfirmationImage(models.Model):
    image = models.ImageField(upload_to="confirmation/")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    challenge = models.ForeignKey("Challenge", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name} {self.date}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
