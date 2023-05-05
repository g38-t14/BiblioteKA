from rest_framework import serializers

from .models import Follower


class FollowerSerializer(serializers.ModelSerializer):
    user_id = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        book_id = validated_data.get("book_id")
        return super().create(validated_data)

    class Meta:
        model = Follower
        fields = [
            "id",
            "book_id",
            "user_id",
        ]
        depth = 1