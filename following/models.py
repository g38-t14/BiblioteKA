from django.db import models


class Follower(models.Model):
    book = models.ForeignKey(
        "books.book",
        on_delete=models.CASCADE,
        related_name="book_following"
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="user_book_follower"
    )

    class Meta:
        unique_together = ["book", "user"]