from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    student_id = models.CharField(
        max_length=20, unique=True, help_text="Unique student ID / Roll number"
    )
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.student_id} - {self.first_name} {self.last_name}"
