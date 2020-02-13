from django.db import models

class TrainingProgram(models.Model):
    title = models.CharField(max_length=25)
    description = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    capacity = models.IntegerField()