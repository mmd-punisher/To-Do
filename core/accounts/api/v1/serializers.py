from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework import serializers

from accounts.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150, validators=[]
    )  # Showing serializer username validation error first
    email = serializers.EmailField(validators=[])
    password1 = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "password1",
        )

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")

        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("This email is already registered.")

        return value

    def validate(self, attrs):
        password = attrs.get("password")
        password1 = attrs.get("password1")
        if password != password1:
            raise serializers.ValidationError({"password": "Passwords must match."})
        try:
            validate_password(password)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("password1", None)
        return User.objects.create_user(**validated_data)
