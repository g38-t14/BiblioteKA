from rest_framework import serializers
from .models import Copy


class CopySerializers(serializers.ModelSerializer):
    class Meta:
        model: Copy
        fields = [
            "id",
            "books_id",
            "available",
        ]
