from django.db import models
from patient.models import Patient
from doctor.models import Doctor

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return f"{self.patient.name} - {self.doctor.name} on {self.date}"
