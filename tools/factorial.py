def factorial(n: int) -> int:
    """Calculate the factorial of a number."""
    
    if n == 0:
        return 1
    return n * factorial(n - 1)