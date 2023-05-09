from rest_framework import serializers
from .models import Loan


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = [
            "copy",
            "loaner",
            "return_date",
            "returned",
        ]
        read_only_fields = [
            "copy",
            "loaner",
            "return_date",
            "returned",
        ]


class ReturnLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = [
            "copy",
            "loaner",
            "return_date",
            "returned",
        ]
        read_only_fields = [
            "copy",
            "loaner",
            "return_date",
        ]
