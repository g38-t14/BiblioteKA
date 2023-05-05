from django.db import models


class Copy(models.Model):
    class Meta:
        ordering = ("id",)

    book = models.ForeignKey(
        "books.Book",
        on_delete=models.CASCADE,
        related_name="copies"
    )

    available = models.BooleanField(default=True)
