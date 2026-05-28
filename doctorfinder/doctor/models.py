from django.db import models

# Create your models here
class Doctor(models.Model):
    user_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)
    experience = models.IntegerField()
    fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return  self.name
