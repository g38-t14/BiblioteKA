from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    STUDENT = "student"
    EMPLOYEE = "employee"


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=127, unique=True)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    is_blocked = models.BooleanField(null=True, default=False)

    role = models.CharField(max_length=20, choices=UserRole.choices)
