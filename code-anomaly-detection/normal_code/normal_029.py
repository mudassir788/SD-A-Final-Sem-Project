"""String formatting utilities."""

def format_currency(amount):
    """Format amount as currency."""
    return f"${amount:.2f}"

def truncate_string(text, length):
    """Truncate string to length."""
    if len(text) <= length:
        return text
    return text[:length-3] + "..."

def capitalize_words(text):
    """Capitalize each word."""
    return " ".join(word.capitalize() for word in text.split())
