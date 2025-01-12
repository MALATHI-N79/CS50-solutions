# List of coin denominations in cents
arr = [25, 10, 5, 1]
ans = []

# Prompt the user for the change owed
while True:
    try:
        n = float(input("Change owed: ")) * 100
        if n >= 0:
            n = int(round(n))
            break
    except ValueError:
        pass

# Calculate the minimum number of coins
for coin in arr:
    while n >= coin:
        n -= coin
        ans.append(coin)

print("Coins used:")
for coin in ans:
    print(coin, end=" ")
print()

print("The minimum number of coins is", len(ans))
print("The coins are:", " ".join(map(str, ans)))