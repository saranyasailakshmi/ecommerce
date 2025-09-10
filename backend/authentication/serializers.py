from rest_framework import serializers
from django.contrib.auth import get_user_model
from .validators import validate_email, validate_password, validate_role

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={"input_type": "password"}, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, style={"input_type": "password"})
    email = serializers.EmailField(validators=[validate_email])
    role = serializers.CharField(validators=[validate_role])

    class Meta:
        model = User
        fields = ["email", "password", "confirm_password", "role"]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "role"]