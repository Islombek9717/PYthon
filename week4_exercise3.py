balance = 1000
account_blocked = False
withdraws = [200, 500, 400]
for amount in withdraws:
    if account_blocked:
        print("Account is blocked. Withdrawal not allowed.")
    break
if balance >= amount:
    balance -= amount
    print(f"Withdrawal of {amount} successful. New balance: {balance}")
else:
    print(
        f"Insufficient funds for withdrawal of {amount}. Current balance: {balance}")
