from django.db import models
from django.contrib.auth.models import AbstractUser


class UserRole(models.TextChoices):
    STUDENT = "student"
    EMPLOYEE = "employee"


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=255, unique=True)

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    is_blocked = models.BooleanField(null=True, default=False)
    block_date = models.DateField(null=True, default=None)

    role = models.CharField(max_length=20, choices=UserRole.choices)
