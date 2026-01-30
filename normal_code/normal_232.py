"""String utility functions."""

def reverse_string(text):
    """Reverse a string."""
    return text[::-1]

def count_vowels(word):
    """Count vowels in a word."""
    vowels = "aeiouAEIOU"
    return sum(1 for char in word if char in vowels)

def clean_string(text):
    """Remove extra whitespace."""
    return " ".join(text.split())
