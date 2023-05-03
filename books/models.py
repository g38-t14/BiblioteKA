from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    author = models.CharField(max_length=100)

    users_following = models.ManyToManyField(
        "users.User", related_name="books_following"
    )
