from django.contrib.auth.models import User
from django.db import models


class AuthJournal(models.Model):
    name = models.CharField(max_length=500)
    surname = models.CharField(max_length=500)
    username = models.CharField(max_length=500)
    password = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.surname} {self.name}"


class ConfirmationImage(models.Model):
    image = models.ImageField(upload_to="confirmation/")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name} {self.date}"
