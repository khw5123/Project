n = int(input())
a, b = [], []
for i in range(2):
    s = input()
    for j in range(n):
        if i == 0:
            a.append(int(s.split()[j]))
        else:
            b.append(int(s.split()[j]))
a.sort()
b.sort(reverse=True)
result = 0
for i in range(n):
    result += a[i] * b[i]
print(result)