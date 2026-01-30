"""File handling utilities."""

def read_lines(filepath):
    """Read file lines."""
    try:
        with open(filepath, 'r') as f:
            return f.readlines()
    except FileNotFoundError:
        return []

def count_lines(filepath):
    """Count lines in file."""
    try:
        with open(filepath, 'r') as f:
            return len(f.readlines())
    except Exception:
        return 0
