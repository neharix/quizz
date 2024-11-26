from django.contrib.auth.models import User
from django.db import models


class AuthJournal(models.Model):
    name = models.CharField(max_length=500)
    surname = models.CharField(max_length=500)
    username = models.CharField(max_length=500)
    password = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.surname} {self.name}"
