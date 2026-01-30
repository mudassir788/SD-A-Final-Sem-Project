"""List manipulation functions."""

def remove_duplicates(items):
    """Remove duplicates from list."""
    return list(dict.fromkeys(items))

def find_max(numbers):
    """Find maximum number."""
    if not numbers:
        return None
    return max(numbers)

def rotate_list(lst, n):
    """Rotate list by n positions."""
    if not lst:
        return lst
    n = n % len(lst)
    return lst[-n:] + lst[:-n]
