from django.db import models


class Followers(models.Model):
    book = models.ForeignKey(
        "books.book",
        on_delete=models.CASCADE,
        related_name="book_following"
    )
    follower = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="user_book_follower"
    )
