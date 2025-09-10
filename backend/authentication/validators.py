from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


def validate_email(value):
    if value is None:
        raise ValidationError("Email cannot be null.")
    if value.strip() == "":
        raise ValidationError("Email cannot be blank.")
    if User.objects.filter(email=value).exists():
        raise ValidationError("This email is already registered.")
    return value


def validate_password(value):
    if value is None:
        raise ValidationError("Password cannot be null.")
    if value.strip() == "":
        raise ValidationError("Password cannot be blank.")
    if len(value) < 6:
        raise ValidationError("Password must be at least 6 characters long.")
    return value


def validate_role(value):
    if value is None:
        raise ValidationError("Role cannot be null.")
    if value.strip() == "":
        raise ValidationError("Role cannot be blank.")
    if value not in ["customer", "seller"]:
        raise ValidationError("Role must be either 'customer' or 'seller'.")
    return value
