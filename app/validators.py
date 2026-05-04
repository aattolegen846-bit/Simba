import re
from typing import Optional


class ValidationError(ValueError):
    """Custom validation error"""
    pass


def validate_email(email: str) -> str:
    """Validate email format"""
    if not email or not isinstance(email, str):
        raise ValidationError("Email is required")

    email = email.strip().lower()

    if len(email) > 254:
        raise ValidationError("Email is too long")

    # Basic email regex
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError("Invalid email format")

    return email


def validate_username(username: str) -> str:
    """Validate username format"""
    if not username or not isinstance(username, str):
        raise ValidationError("Username is required")

    username = username.strip()

    if len(username) < 3:
        raise ValidationError("Username must be at least 3 characters")

    if len(username) > 50:
        raise ValidationError("Username is too long (max 50 characters)")

    # Only alphanumeric, underscore, hyphen
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        raise ValidationError("Username can only contain letters, numbers, underscore and hyphen")

    return username


def validate_password(password: str) -> str:
    """Validate password strength"""
    if not password or not isinstance(password, str):
        raise ValidationError("Password is required")

    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters")

    if len(password) > 128:
        raise ValidationError("Password is too long (max 128 characters)")

    # Check for at least one digit and one letter
    if not re.search(r'[0-9]', password):
        raise ValidationError("Password must contain at least one digit")

    if not re.search(r'[a-zA-Z]', password):
        raise ValidationError("Password must contain at least one letter")

    return password


def validate_string_length(value: str, field_name: str, min_len: int = 1, max_len: int = 255) -> str:
    """Validate string length"""
    if not isinstance(value, str):
        raise ValidationError(f"{field_name} must be a string")

    value = value.strip()

    if len(value) < min_len:
        raise ValidationError(f"{field_name} must be at least {min_len} characters")

    if len(value) > max_len:
        raise ValidationError(f"{field_name} is too long (max {max_len} characters)")

    return value


def sanitize_string(value: str, max_len: int = 1000) -> str:
    """Sanitize string input to prevent injection attacks"""
    if not isinstance(value, str):
        return str(value)[:max_len]

    # Remove null bytes
    value = value.replace('\x00', '')

    # Limit length
    return value[:max_len]
