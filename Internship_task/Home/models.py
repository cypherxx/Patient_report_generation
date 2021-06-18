from django.db import models
from django.contrib.auth.models import User,AbstractUser

class CustomUser(AbstractUser):

    contact = models.CharField(max_length=15)

    class Meta:
        ordering = ('-id',)

    def __str__(self):

        return f'{self.first_name}'

class Report_Patient(models.Model):

    patient = models.CharField(max_length=100)
    report = models.FileField(upload_to='media')