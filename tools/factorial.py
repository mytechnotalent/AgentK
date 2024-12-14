# MIT License

# Copyright (c) 2024 My Techno Talent

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


def factorial(n: int) -> int:
    """
    Calculate the factorial of a non-negative integer.

    The factorial of a number `n` is defined as the product of all positive 
    integers from `1` to `n`. For `n = 0`, the factorial is defined as `1`.

    This function uses recursion to calculate the factorial, with the base case 
    being `n = 0`.

    Args:
        n (int): A non-negative integer for which the factorial is to be calculated.

    Returns:
        int: The factorial of the given number `n`.

    Raises:
        RecursionError: If the recursion limit is exceeded (e.g., for very large `n`).
        ValueError: If `n` is a negative integer.
    """
    
    if n < 0:
        raise ValueError("Factorial is not defined for negative integers.")
    if n == 0:
        return 1
    return n * factorial(n - 1)