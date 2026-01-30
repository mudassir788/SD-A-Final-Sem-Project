"""Type validation functions."""

def is_numeric(value):
    """Check if value is numeric."""
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False

def is_valid_email(email):
    """Basic email validation."""
    return "@" in email and "." in email

def type_name(obj):
    """Get type name of object."""
    return type(obj).__name__
