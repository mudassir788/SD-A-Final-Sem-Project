"""Dictionary helper functions."""

def merge_dicts(dict1, dict2):
    """Merge two dictionaries."""
    result = dict1.copy()
    result.update(dict2)
    return result

def invert_dict(mapping):
    """Invert keys and values."""
    return {v: k for k, v in mapping.items()}

def get_keys_by_value(data, value):
    """Get all keys with specific value."""
    return [k for k, v in data.items() if v == value]
