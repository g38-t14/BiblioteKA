from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    author = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    max_loan_time = models.IntegerField(default=7)

    users_following = models.ManyToManyField(
        "users.User",
        through="following.BookFollowers",
        related_name="books_following", 
        null=True
    )
