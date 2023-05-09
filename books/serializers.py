from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "title",
            "description",
            "author",
            "quantity",
            "max_loan_time",
            "users_following",
        ]
