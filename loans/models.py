from django.db import models


# Create your models here.
class Loan(models.Model):
    copy = models.ForeignKey(
        "copies.Copy",
        on_delete=models.CASCADE,
        related_name="copy_loan",
    )
    loaner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="user_copy_loan",
    )

    return_date = models.DateTimeField()
