from rest_framework import serializers
from .models import User
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        print(validated_data)
        if validated_data["role"] == "employee":
            return User.objects.create_superuser(**validated_data)

        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data):
        new_password = validated_data.pop("password")
        if new_password:
            instance.set_password(new_password)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_blocked",
            "role",
            "block_date",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "is_blocked": {"write_only": True},
            "block_date": {"write_only": True},
            "username": {
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message="A user with that username already exists.",
                    )
                ]
            },
            "email": {
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all(), message="Email already registered."
                    )
                ],
            },
        }
