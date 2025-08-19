import math

# 1. Read integer values of x and y from STDIN
x = int(input("Enter value for x: "))
y = int(input("Enter value for y: "))

# 2. Declare a variable z = x^y
z = x ** y

# 3. Declare a variable result = sqrt(z)
result = math.sqrt(z)

# 4. Print results, formatted to 2 decimal points
print(f"x^y = {z:.2f}")
print(f"Square root of z = {result:.2f}")
