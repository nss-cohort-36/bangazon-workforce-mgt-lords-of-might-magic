from django.db import models

class TrainingProgramEmployee(models.Model):
    employee = models.ForeignKey("Employee", on_delete=models.CASCADE)
    training_program = models.ForeignKey("TrainingProgram", on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("TrainingProgramEmployee")
        verbose_name_plural = ("TrainingProgramEmployees")