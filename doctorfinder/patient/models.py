from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    user_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
