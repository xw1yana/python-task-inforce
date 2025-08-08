from django.contrib.auth.models import AbstractUser
from django.db import models


class Employee(AbstractUser):
    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
