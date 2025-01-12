# Prompt the user for the pyramid's height
while True:
    try:
        n = int(input("Height: "))
        if 1 <= n <= 8:
            break
    except ValueError:
        pass

# Build the pyramid
for i in range(1, n + 1):
    print(" " * (n - i) + "#" * i)