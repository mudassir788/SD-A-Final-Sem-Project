"""Set manipulation functions."""

def common_elements(set1, set2):
    """Find common elements."""
    return set1 & set2

def unique_elements(set1, set2):
    """Find unique elements."""
    return set1 ^ set2

def superset_check(set1, set2):
    """Check if set1 is superset of set2."""
    return set1 >= set2
