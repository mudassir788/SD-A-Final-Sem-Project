"""Module for data processing utilities."""

def process_list(items):
    """Process a list of items."""
    return [x * 2 for x in items if x > 0]

def sum_values(data):
    """Calculate sum of values."""
    total = sum(data)
    return total

if __name__ == "__main__":
    test_data = [1, 2, 3, 4, 5]
    print(process_list(test_data))