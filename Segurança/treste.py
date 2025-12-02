n = 9
total = 0

x = 1
while x < n:
    for y in range(x):
        for z in range(y, n):
            total += 1
    x *= 2

print(f"Total de execuções: {total}")
