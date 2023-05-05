from rest_framework import serializers

from .models import Follower


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = [
            "id",
            "book",
            "user",
        ]
        read_only_fields = [
            "id",
            "book",
            "user",
        ]
        # depth = 1