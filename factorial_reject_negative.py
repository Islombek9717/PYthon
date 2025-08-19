# Read input from the user
n = int(input("Enter a number to calculate its factorial: "))

# Check for negative numbers
if n < 0:
    print("Error: Factorial of a negative number does not exist.")
# Check if the number is too large
elif n > 20:
    print("Too large to calculate")
else:
    # Initialize factorial
    factorial = 1
    # Calculate factorial using a for loop
    for i in range(1, n + 1):
        factorial *= i
    # Print the result
    print(f"The factorial of {n} is {factorial}")
