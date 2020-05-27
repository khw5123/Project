a, b = map(str, input().split())
answer = len(b)
for i in range(len(b)-len(a)+1):
    count = 0
    for j in range(len(a)):
        if b[i+j] != a[j]:
            count += 1
    answer = min(answer, count)
print(answer)