from rest_framework import serializers
from .models import Copy


class CopySerializers(serializers.ModelSerializers):
    class Meta:
        model: Copy
        fields = [
            "id",
            "max_loan_time",
            "books_id"
        ]
