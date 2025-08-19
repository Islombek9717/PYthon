# Read input from the user
n = int(input("Enter a number to calculate its factorial: "))

# Initialize factorial
factorial = 1

# Calculate factorial using a for loop
for i in range(1, n + 1):
    factorial *= i

# Print the result
print(f"The factorial of {n} is {factorial}")
