balance = 1000
withdraw = 200
account_blocked = False
if not account_blocked:
    if withdraw <= balance:
        balance -= withdraw
        print(f"Withdrawal successful. New balance: {balance}")
    else:
        print("Insufficient funds for withdrawal.")
else:
    print("Account is blocked. Withdrawal not allowed.")
