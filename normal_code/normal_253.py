"""Mathematical utilities."""

def factorial(n):
    """Calculate factorial of n."""
    if n < 0:
        return None
    if n == 0:
        return 1
    return n * factorial(n - 1)

def is_prime(num):
    """Check if number is prime."""
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True
