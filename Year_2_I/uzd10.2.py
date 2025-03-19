# Initialize the first two Fibonacci numbers
a, b = 1, 2
even_sum = 0

# Loop to generate Fibonacci numbers up to four million
while a <= 4000000:
    # Add to the sum if the Fibonacci number is even
    if a % 2 == 0:
        even_sum += a
    # Move to the next Fibonacci number
    a, b = b, a + b

# Print the result
print(even_sum)
