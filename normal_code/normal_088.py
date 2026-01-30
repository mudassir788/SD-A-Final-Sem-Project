"""Iteration utility functions."""

def chunked_list(items, size):
    """Split list into chunks."""
    return [items[i:i+size] for i in range(0, len(items), size)]

def enumerate_items(collection):
    """Enumerate with index."""
    for idx, item in enumerate(collection):
        yield idx, item

def flatten(nested_list):
    """Flatten nested list."""
    return [item for sublist in nested_list for item in sublist]
