def is_palindrome(num):
    """Check if a number is a palindrome."""
    return str(num) == str(num)[::-1]

def print_palindromes(limit):
    """Print all palindrome numbers up to the given limit."""
    for num in range(limit):
        if is_palindrome(num):
            print(num)

# Define the limit (2^31)
limit = 2**31

# Call the function to print palindromes
print_palindromes(limit)

